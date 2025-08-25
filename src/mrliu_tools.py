try:
    import json, os, re, click
    from tools import resource
    from tools.resource import help_
except:
    import tools.pkg_installer as pkg_installer
    pkg_installer.required = ["click"]
    pkg_installer.check()

    import click
    click.secho("Successfully install!")
    click.secho("Use 'mrliu_tools' for help", fg="cyan")
    exit()


__version__ = "1.3.2"


tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
lang = resource.lang
(rn, ad, sl) = (help_("rename", lang)["options"], help_("audio", lang)["options"], help_("set_language", lang)["options"])


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, message="MrLiu Tools Version: %(version)s")
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        display_welcome_message()


def display_welcome_message():
    for i in resource.icon_command["text_lines"]:
        charIndex = 0
        for char in i:
            colorIndex = (charIndex // 2) % len(resource.icon_command["colors"])
            click.secho(char, fg=resource.icon_command["colors"][colorIndex], nl=False)
            charIndex += 1
        click.secho("")
    if lang == "en":
        click.secho(" - A collection of useful command line tools.", fg="cyan")
        click.secho("Use 'mrliu_tools rename --help' for more information on the rename tool.", fg="cyan")
        click.secho("Use 'mrliu_tools audio --help' for more information on the audio tool.", fg="cyan")
        click.secho("Use 'mrliu_tools set-language zh/en' to change the language of help.", fg="cyan")
        click.secho("Use 'mrliu_tools --help' for more information on other tools.", fg="cyan")
        click.secho()
    else:
        click.secho(" - 实用的命令行工具.", fg="cyan")
        click.secho("输入 'mrliu_tools rename --help' 获取更多关于rename工具的信息.", fg="cyan")
        click.secho("输入 'mrliu_tools audio --help' 获取更多关于audio工具的信息.", fg="cyan")
        click.secho("输入 'mrliu_tools set-language zh/en' 更改帮助语言.", fg="cyan")
        click.secho("输入 'mrliu_tools --help' 获取更多关于其他工具的信息.", fg="cyan")
        click.secho()


def extract_version(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'^__version__\s*=\s*["\'](.*?)["\']', content, re.MULTILINE)
    if match:
        return match.group(1)
    else:
        return "None"


@cli.command(help=help_("rename", lang)["description"])
@click.option("-p", "--path", default=".", help=rn["-p"])
@click.option("-pt", "--pattern", default=".*", help=rn["-pt"])
@click.option("-t", "--to", default="?name;-?rand=6;?ext;", help=rn["-t"])
@click.option("-wd", "--with-dir", is_flag=True, help=rn["-wd"])
@click.option("-od", "--only-dir", is_flag=True, help=rn["-od"])
@click.option("-r", "--restore", is_flag=True, help=rn["-r"])
@click.option("--more-help", is_flag=True, help=rn["--more-help"])
@click.version_option(version=extract_version(os.path.join(tools_path, "rename_tool.py")), message="Rename Tool Version: %(version)s")
def rename(path, pattern, to, with_dir, only_dir, restore, more_help):
    from tools import rename_tool
    rename_tool.__really_rename__ = True
    if more_help:
        click.echo(resource.more_help[lang])
        return

    if restore:
        rename_tool.restore(os.path.abspath(path))
        return

    if with_dir and only_dir:
        click.echo("[Warning]You cannot choose '--with-dir' and '--only-dir' at the same time", fg="yellow")
        return
    try:
        files_list = os.listdir(path)
    except:
        click.secho("[Error]dir name is not valid", fg="red")
        return
    if not files_list:
        click.secho("[Error]No files found in the specified directory.", fg="red")
        return

    click.secho("The directory to be renamed is: ", nl=False)
    click.secho(os.path.abspath(path), fg="cyan")
    click.secho("Do you really want to rename it[Y/n]: ", fg="yellow", nl=False)
    if input() not in ["Y", "y"]: return

    click.secho("Starting renaming...", fg="green")
    for i in range(len(files_list)-1, -1, -1):
        isfile = os.path.isfile(os.path.join(path, files_list[i]))
        m = True
        if only_dir: m = False if isfile else True
        elif not only_dir and not with_dir: m = True if isfile else False

        if not m or not re.match(pattern=pattern, string=files_list[i]):
            files_list.pop(i)
    rename_tool.rename(files_list, os.path.abspath(path), to)


@cli.command(help=help_("audio", lang)["description"])
@click.option("-i", "--ip", default="None", help=ad["--ip"])
@click.option("-p", "--port", default=50007, help=ad["--port"])
@click.option("-r", "--rate", default=48000, help=ad["--rate"])
@click.option("--channels", default=2, help=ad["--channels"])
@click.option("--chunk", default=1024, help=ad["--chunk"])
@click.option("--send", is_flag=True, help=ad["--send"])
@click.option("--recv", is_flag=True, help=ad["--recv"])
@click.version_option(version=extract_version(os.path.join(tools_path, "audio_tool.py")), message="Audio Tool Version: %(version)s")
def audio(ip, port, rate, channels, chunk, send, recv):
    from tools import audio_tool
    if send: audio_tool.audio_send(ip, port, rate, channels, chunk)
    if recv: audio_tool.audio_recv(port, rate, channels, chunk)


@cli.command(help=help_("set_language", lang)["description"])
@click.argument("lang", type=click.Choice(["en", "zh"], case_sensitive=False))
def set_language(lang):
    """设置命令行工具的语言(en/zh)"""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "r") as f:
        js = json.load(f)
    js["language"] = lang
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "w") as f:
        json.dump(js, f, indent=4)
    click.secho(f"Language set to {lang}", fg="green")


if __name__ == "__main__":
    cli()
