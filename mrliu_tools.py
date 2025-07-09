try:
    import re, os, click, json
    import pyaudio

    from tools import rename_tool, resource, audio_tool
    from tools.resource import help_
except:
    import pkg_installer
    pkg_installer.check()
    print("Successfully install!")
    print("Use 'mrliu_tools' for help")
    exit()


lang = resource.lang
(rn, ads, adr, sl) = (help_("rename", lang)["options"], help_("audio_send", lang)["options"],
    help_("audio_recv", lang)["options"], help_("set_language", lang)["options"])


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        display_welcome_message()


@cli.command(help=help_("rename", lang)["description"])
@click.option("-p", "--path", default=".", help=rn["-p"])
@click.option("-pt", "--pattern", default=".*", help=rn["-pt"])
@click.option("-t", "--to", default="?name;-?rand=6;?ext;", help=rn["-t"])
@click.option("-wd", "--with-dir", is_flag=True, help=rn["-wd"])
@click.option("-od", "--only-dir", is_flag=True, help=rn["-od"])
@click.option("-r", "--restore", is_flag=True, help=rn["-r"])
@click.option("--more-help", is_flag=True, help=rn["--more-help"])
@click.version_option(version=rename_tool.__version__, message="Rename Tool Version: %(version)s")
def rename(path, pattern, to, with_dir, only_dir, restore, more_help):
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


@cli.command(help=help_("audio_send", lang)["description"])
@click.argument("receiver_ip")
@click.option("--port", default=50007, help=ads["--port"])
@click.option("--rate", default=48000, help=ads["--rate"])
@click.option("--channels", default=2, help=ads["--channels"])
@click.option("--chunk", default=1024, help=ads["--chunk"])
def audio_send(receiver_ip, port, rate, channels, chunk):
    audio_tool.audio_send(receiver_ip, port, rate, channels, chunk)


@cli.command(help=help_("audio_recv", lang)["description"])
@click.option("--port", default=50007, help=adr["--port"])
@click.option("--rate", default=48000, help=adr["--rate"])
@click.option("--channels", default=2, help=adr["--channels"])
@click.option("--chunk", default=1024, help=adr["--chunk"])
def audio_recv(port, rate, channels, chunk):
    audio_tool.audio_recv(port, rate, channels, chunk)


@cli.command(help=help_("set_language", lang)["description"])
@click.argument("lang", type=click.Choice(["en", "zh"], case_sensitive=False))
def set_language_cmd(lang):
    """设置命令行工具的语言(en/zh)"""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "r") as f:
        js = json.load(f)
    js["language"] = lang
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "w") as f:
        json.dump(js, f, indent=4)
    click.secho(f"Language set to {lang}", fg="green")


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
        click.secho("Use 'mrliu_tools audio-send --help' for more information on the audio-send tool.", fg="cyan")
        click.secho("Use 'mrliu_tools audio-recv --help' for more information on the audio-recv tool.", fg="cyan")
        click.secho("Use 'mrliu_tools set-language-cmd zh/en' to change the language of help.", fg="cyan")
        click.secho("Use 'mrliu_tools --help' for more information on other tools.", fg="cyan")
    else:
        click.secho(" - 实用的命令行工具.", fg="cyan")
        click.secho("输入 'mrliu_tools rename --help' 获取更多关于rename工具的信息.", fg="cyan")
        click.secho("输入 'mrliu_tools audio-send --help' 获取更多关于audio-send工具的信息.", fg="cyan")
        click.secho("输入 'mrliu_tools audio-recv --help' 获取更多关于audio-recv工具的信息.", fg="cyan")
        click.secho("输入 'mrliu_tools set-language-cmd zh/en' 更改帮助语言.", fg="cyan")
        click.secho("输入 'mrliu_tools --help' 获取更多关于其他工具的信息.", fg="cyan")


if __name__ == "__main__":
    cli()
