# Notes

## First Steps

1. Clone repo via SSH 

```sh
git clone git@github.com:digitalhabitat/bot2_ros2_workspace.git
```

or

```sh
git clone --recurse-submodules git@github.com:digitalhabitat/bot2_ros2_workspace.git
```

2. Run task in import repos `Ctrl+Shift+P` **Import from workspaces file**

> [!NOTE]
> The Source Control section in vscode will detect if the version that your subproject is at, is
> different from the version committed in the superproject's tree. This happends because vcs-tool
> imports the version defined in the .repos file which will typically be more up-to-date.
>
> If you want to use the version that was associated with the superproject's tree you can use
> `git submodule update --init --recursive`
> 
> For details see:
> https://git-scm.com/book/en/v2/Git-Tools-Submodules
> https://stackoverflow.com/questions/6006494/git-submodule-modified-files-status


## ros topic example to control blink1 

Blinking amber bottom led

```sh
ros2 topic pub --once /string_topic std_msgs/msg/String "data: 'pattern/play?pattern=0,ffbf00,0.4,2,000000,0.4,2'"
```
Server tickle demo

```sh
ros2 topic pub /string_topic std_msgs/msg/String "data: 'servertickle/on'"
```
Server tickle demo

```sh
ros2 topic pub /string_topic std_msgs/msg/String "data: 'servertickle/on?time=5'"
```

turn off top LED

```sh
ros2 topic pub --once /string_topic std_msgs/msg/String "data: 'fadeToRGB?rgb=000000&ledn=1'"
```

turn on top LED to red
```sh
ros2 topic pub --once /string_topic std_msgs/msg/String "data: 'fadeToRGB?rgb=F00000&ledn=1'"
```

turn off LED

```sh
ros2 topic pub --once /string_topic std_msgs/msg/String "data: 'fadeToRGB?rgb=000000&ledn=0'"
```

blink purple three times then turn off

```sh
ros2 topic pub --once /string_topic std_msgs/msg/String "data: 'blink?rgb=FF00FF'"
```