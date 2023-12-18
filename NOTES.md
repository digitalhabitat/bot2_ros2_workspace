# ros topic example to control blink1 

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