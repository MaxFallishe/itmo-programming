#  type: ignore
import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        cut = self.ino & 0xFFFFFFFF
        head = struct.pack(
            "!LLLLLLLLLL20sH",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            cut,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
        )
        name = self.name.encode()
        n = 0
        pack = head + name + b"\x00" * n
        while len(pack) % 8 != 0:
            n += 1
            pack = head + name + b"\x00" * n
        return pack

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        roof = data[:62]
        unpack = struct.unpack("!LLLLLLLLLL20sH", roof)
        named = data[62 : len(data)].decode().rstrip("\x00")
        result = GitIndexEntry(
            ctime_s=unpack[0],
            ctime_n=unpack[1],
            mtime_s=unpack[2],
            mtime_n=unpack[3],
            dev=unpack[4],
            ino=unpack[5],
            mode=unpack[6],
            uid=unpack[7],
            gid=unpack[8],
            size=unpack[9],
            sha1=unpack[10],
            flags=unpack[11],
            name=named,
        )
        return result


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not os.path.isfile(pathlib.Path(gitdir, "index")):
        return []
    with open(pathlib.Path(gitdir, "index"), "rb") as f:
        bytearray = []
        while True:
            byte = f.read(1)
            bytearray.append(byte)
            if not byte:
                break
        head = b"".join(bytearray[0:4])
        version = int.from_bytes(b"".join(bytearray[4:8]), "big")
        qty = int.from_bytes(b"".join(bytearray[8:12]), "big")
        payload = bytearray[12 : len(bytearray) - 21]
        indexsha = b"".join(bytearray[len(bytearray) - 21 : len(bytearray) - 1])
    n = 61
    start = 0
    objs = []
    lens = []
    for i in range(len(payload)):
        check1 = i - 1 > n and (i + 1) % 8 == 0
        check3 = payload[i] == b"\x00"
        check4 = False
        try:
            payload[i + 2].decode()
        except Exception as e:
            check4 = True
        if (check1 and check3) or (check1 and check4):
            objs.append(payload[start : i + 1])
            lens.append(len(payload[start:i]) + 1)
            n += len(payload[start : i + 1])  # do i really need 1?
            start = i + 1
            if len(objs) == qty:
                break
    result = []
    names = []
    for i in range(qty):
        names.append(b"".join(objs[i][62:]).strip(b"\x00").decode("Windows-1251"))
    for i in range(qty):
        x = GitIndexEntry.unpack(b"".join(objs[i][0:62]))
        result.append(
            GitIndexEntry(
                ctime_s=x.ctime_s,
                ctime_n=x.ctime_n,
                mtime_s=x.mtime_s,
                mtime_n=x.mtime_n,
                dev=x.dev,
                ino=x.ino,
                mode=x.mode,
                uid=x.uid,
                gid=x.gid,
                size=x.size,
                sha1=x.sha1,
                flags=x.flags,
                name=names[i],
            )
        )
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    sign = b"DIRC"
    version = 2
    roof = struct.pack("!4sLL", sign, version, len(entries))
    all_payload = []
    for i in entries:
        all_payload.append(GitIndexEntry.pack(i))
    payload_joined = b"".join(all_payload)
    data = roof + payload_joined
    diest = hashlib.sha1(data).digest()
    with open(pathlib.Path(gitdir, "index"), "wb") as f:
        f.write(data + diest)
        f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    objects = read_index(gitdir)
    resultdet = []
    if details:
        res = []
        for i in objects:
            res.append(["100644", i.sha1.hex(), "0", str(i.name).strip()])
        for j in res:
            resultdet.append(f"{j[0]} {j[1]} {j[2]}\t{j[3]}")
        for k in resultdet:
            print(k)
    else:
        result = []
        for object_ in objects:
            result.append(object_.name)
        print(*result, sep="\n")


def update_index(
    gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True
) -> None:
    entrances = read_index(gitdir)
    for path in paths:
        with path.open("rb") as f:
            data = f.read()
        stat = os.stat(path)
        entrances.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash_object(data, "blob", write=True)),
                flags=7,
                name=str(path),
            )
        )
    if write:
        write_index(gitdir, sorted(entrances, key=lambda x: x.name))
