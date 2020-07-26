SET_WEBDRIVER = '''() => {Object.defineProperty(navigator, 'webdriver', {get: () => undefined})}'''
SET_USER_AGENT = '''() => {Object.defineProperty(navigator, 'userAgent', {get: () => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})}'''
SET_APP_VERSION = '''() => {Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})}'''
EXTEND_LANGUAGES = '''() => {Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en', 'zh-TW', 'ja']})}'''
EXTEND_PLUGINS = '''() => {Object.defineProperty(navigator, 'plugins', {get: () => [0, 1, 2, 3, 4]})}'''
EXTEND_MIME_TYPES = '''() => {Object.defineProperty(navigator, 'mimeTypes', {get: () => [0, 1, 2, 3, 4]})}'''
SET_WEBGL = '''() => {
    const getParameter = WebGLRenderingContext.getParameter
    WebGLRenderingContext.prototype.getParameter = (parameter) => {
      if (parameter === 37445) {
        return 'Intel Open Source Technology Center'
      }
      if (parameter === 37446) {
        return 'Mesa DRI Intel(R) Ivybridge Mobile '
      }
      return getParameter(parameter)
    }
  }
'''
SET_CHROME_INFO = '''() => {
  Object.defineProperty(window, 'chrome', {
    "app": {
      "isInstalled": false,
      "InstallState": {"DISABLED": "disabled", "INSTALLED": "installed", "NOT_INSTALLED": "not_installed"},
      "RunningState": {"CANNOT_RUN": "cannot_run", "READY_TO_RUN": "ready_to_run", "RUNNING": "running"}
    },
    "runtime": {
      "OnInstalledReason": {
        "CHROME_UPDATE": "chrome_update",
        "INSTALL": "install",
        "SHARED_MODULE_UPDATE": "shared_module_update",
        "UPDATE": "update"
      },
      "OnRestartRequiredReason": {"APP_UPDATE": "app_update", "OS_UPDATE": "os_update", "PERIODIC": "periodic"},
      "PlatformArch": {
        "ARM": "arm",
        "ARM64": "arm64",
        "MIPS": "mips",
        "MIPS64": "mips64",
        "X86_32": "x86-32",
        "X86_64": "x86-64"
      },
      "PlatformNaclArch": {"ARM": "arm", "MIPS": "mips", "MIPS64": "mips64", "X86_32": "x86-32", "X86_64": "x86-64"},
      "PlatformOs": {
        "ANDROID": "android",
        "CROS": "cros",
        "LINUX": "linux",
        "MAC": "mac",
        "OPENBSD": "openbsd",
        "WIN": "win"
      },
      "RequestUpdateCheckStatus": {
        "NO_UPDATE": "no_update",
        "THROTTLED": "throttled",
        "UPDATE_AVAILABLE": "update_available"
      }
    }
  })
}
'''

SET_PERMISSION = '''() => {
  const originalQuery = window.navigator.permissions.query;
  return window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
      Promise.resolve({ state: Notification.permission }) :
      originalQuery(parameters)
  )
}
'''

SCRIPTS = [
    SET_WEBDRIVER,
    SET_USER_AGENT,
    SET_APP_VERSION,
    EXTEND_LANGUAGES,
    EXTEND_PLUGINS,
    EXTEND_MIME_TYPES,
    SET_CHROME_INFO,
    SET_PERMISSION,
    SET_WEBGL,
]
