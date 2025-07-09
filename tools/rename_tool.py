import re, os, sys, click, json, hashlib
from datetime import datetime


__really_rename__ = False
__version__ = "1.0.7"
__file__ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rename_tool.py")


def restore(path):
    path = path.lower()
    print(os.path.abspath(__file__))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "r") as f:
        js = json.load(f)
        remember = js.get("rename", {})
    if remember and path in remember:
        for i in remember[path]:
            click.secho(i, nl=False)
            click.secho(" -> ", fg="blue", nl=False)
            click.secho(remember[path][i] + " ... ", nl=False)
            if __really_rename__:
                old_name = os.path.join(path, i)
                new_name = os.path.join(path, remember[path][i])
                os.rename(new_name, old_name)

            click.secho("ok", fg="green")
        click.secho("[Information]Restore completed successfully.", fg="green")
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "w") as f:
            del js["rename"][path]
            json.dump(js, f, indent=4)
    else:
        click.secho("[Error]No records found in mrliu_tools.json.", fg="red")


def rename(files_list, path, to):
    path = path.lower()
    count = 1

    if "?time" in to:
        to = re.sub(r"\?time=(.+?);", lambda match: datetime.now().strftime(match.group(1)), to)

    remember = {}
    for i in files_list:
        click.secho(i, nl=False)

        new_name = to
        if "?count" in to:
            new_name = re.sub(r"\?count;", str(count), new_name, flags=re.I)
        new_name = re.sub(r"\?text=(.+?);", r"\1", new_name, flags=re.I)
        new_name = re.sub(r"\?ext;", get_suffix(os.path.join(path, i), i)[1], new_name, flags=re.I)
        new_name = re.sub(r"\?md5;", get_md5(os.path.join(path, i)), new_name, flags=re.I)
        new_name = re.sub(r"\?name;", get_suffix(os.path.join(path, i), i)[0], new_name, flags=re.I)
        new_name = re.sub(r"\?parent;", os.path.basename(os.path.dirname(os.path.join(path, i))), new_name, flags=re.I)
        new_name = re.sub(r"\?user;", os.getenv("USERNAME", "unknown"), new_name, flags=re.I)
        new_name = re.sub(
            r"\?rand=(\d+);", lambda match: ''.join(
            [ "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"[os.urandom(1)[0] % 62] for _ in range(int(match.group(1))) ]
            ), new_name, flags=re.I
        )
        if "?upper;" in new_name:
            new_name = re.sub(r"\?upper;", "", new_name); new_name = new_name.upper()
        if "?lower;" in new_name:
            new_name = re.sub(r"\?lower;", "", new_name); new_name = new_name.lower()
        # more modifiers can be added here...
        count += 1

        click.secho(" -> ", fg="blue", nl=False)
        click.secho(new_name + " ... ", nl=False)
        remember[new_name] = i

        if __really_rename__:
            new_name = os.path.join(path, new_name)
            old_name = os.path.join(path, i)
            os.rename(old_name, new_name)

        click.secho("ok", fg="green")
    click.secho("[Information]Rename completed successfully.", fg="green")
    print(path)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "r") as f:
        js = json.load(f)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "w") as f:
        if "rename" not in js:
            js["rename"] = {}
        if path not in js["rename"]:
            js["rename"][path] = {}
        js["rename"][path] = remember
        json.dump(js, f, indent=4)


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_suffix(file, basename):
    if os.path.isdir(file):
        return os.path.basename(file), ""
    file_ = basename.split(".")
    if len(file_) <= 1: return basename, ""
    else: return basename[:-1-len(file_[-1])], "."+file_[-1]
