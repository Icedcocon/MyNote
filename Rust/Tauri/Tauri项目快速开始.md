# Tauri 项目快速开始

## 一、

### 1. 入口函数

```rust
// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri_app_lib::run()
}
```

- 属性宏 (#![cfg_attr(...)]): 这是一个条件编译的属性宏。
  
  - cfg_attr 是 Rust 中用于条件编译的宏，允许根据条件添加属性。
  
  - not(debug_assertions): 这个条件表示在非调试模式下（即发布模式）应用后面的属性。
  
  - windows_subsystem = "windows": 这个属性告诉编译器在 Windows 系统上编译时，不要创建一个控制台窗口。这通常用于 GUI 应用程序，以避免在启动时弹出一个不必要的命令行窗口。

- fn main(): 这是程序的入口函数。每个可执行的 Rust 程序都必须有一个 main 函数。程序从这里开始执行。

- tauri_app_lib::run(): 这行代码调用了 tauri_app_lib 库中的 run 函数。

### 2. lib 函数

```rust
// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
ication");
}
```

- #[tauri::command]：这是一个属性宏，用于标记 greet 函数，使其可以被 Tauri 的前端 JavaScript 调用。

- fn greet(name: &str) -> String：定义了一个名为 greet 的函数，接受一个字符串切片 name 作为参数，并返回一个 String 类型的值。

- format! 宏：用于格式化字符串，类似于其他语言中的字符串插值。这里它将 name 插入到字符串中，生成一个问候语。

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri appl
    }
```

- #[cfg_attr(mobile, tauri::mobile_entry_point)]：这是一个条件编译属性，表示如果在移动平台上编译，则将 run 函数标记为 Tauri 的移动入口点。

- pub fn run()：定义了一个公共函数 run，它是应用程序的入口点。

- tauri::Builder::default()：创建一个 Tauri 应用程序构建器的默认实例。

- .plugin(tauri_plugin_shell::init())：添加一个插件到 Tauri 应用程序，这里是 tauri_plugin_shell 插件，用于处理 shell 命令。

-  .invoke_handler(tauri::generate_handler![greet])：设置一个调用处理器，允许前端调用 greet 函数。

- .run(tauri::generate_context!())：运行 Tauri 应用程序，使用 generate_context! 宏生成的上下文。

- .expect("error while running tauri application")：如果运行过程中出现错误，程序将会 panic，并输出错误信息。

#### 2.1 插件

Tauri 提供了一些常用的插件，帮助开发者扩展应用程序的功能。以下是一些常见的 Tauri 插件及其用途：

- tauri-plugin-shell：

- 用途：允许应用程序执行系统 shell 命令。这对于需要与操作系统进行交互的应用程序非常有用，比如启动外部程序或脚本。

2. tauri-plugin-window：

- 用途：提供对窗口管理的扩展功能，比如创建、关闭、最小化、最大化窗口等。它可以帮助开发者更灵活地控制应用程序的窗口行为。

- tauri-plugin-dialog：

- 用途：用于显示系统对话框，如文件选择器、消息框等。这使得应用程序可以与用户进行更直观的交互。

- tauri-plugin-notification：

- 用途：允许应用程序发送系统通知。这对于需要提醒用户某些事件或更新的应用程序非常有用。

- tauri-plugin-clipboard：

- 用途：提供对系统剪贴板的访问，允许应用程序复制和粘贴文本或其他数据。

6. tauri-plugin-fs：

- 用途：提供对文件系统的访问，允许应用程序读取和写入文件。这对于需要处理文件数据的应用程序非常重要。

7. tauri-plugin-http：

- 用途：提供 HTTP 客户端功能，允许应用程序进行网络请求。这对于需要与网络服务交互的应用程序非常有用。

- tauri-plugin-auth：

- 用途：提供身份验证功能，帮助应用程序实现用户登录和认证。

## 参考资料
