import os
import importlib.util

PLUGIN_DIR = "plugins"
plugins = {}
disabled_plugins = set()

def load_plugins():
    global plugins
    plugins.clear()
    os.makedirs(PLUGIN_DIR, exist_ok=True)

    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            filepath = os.path.join(PLUGIN_DIR, filename)

            try:
            
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)


                if hasattr(module, "PLUGIN_NAME") and hasattr(module, "TRIGGERS") and hasattr(module, "execute"):
                    name_key = module.PLUGIN_NAME.lower()
                    plugins[name_key] = {
                        "name": module.PLUGIN_NAME,
                        "triggers": module.TRIGGERS,
                        "execute": module.execute
                    }
                    print(f"[ SYSTEM ]: Loaded Plugin -> {module.PLUGIN_NAME}")
            except Exception as e:
                print(f"[ ERROR ]: Failed to load plugin {filename}. Error: {e}")
                
    return len(plugins)

def get_plugin_list():
    return [data["name"] for data in plugins.values()]

def toggle_plugin(name, enable=True):
    name_key = name.lower().strip()
    if name_key in plugins:
        if enable and name_key in disabled_plugins:
            disabled_plugins.remove(name_key)
        elif not enable:
            disabled_plugins.add(name_key)
        return True
    return False

def handle_command(command, speak_callback):
    for key, data in plugins.items():
        if key in disabled_plugins:
            continue
            
        for trigger in data["triggers"]:
            if trigger in command:
                # Execute the plugin and speak its return value
                response = data["execute"](command)
                if response:
                    speak_callback(response)
                return True
                
    return False