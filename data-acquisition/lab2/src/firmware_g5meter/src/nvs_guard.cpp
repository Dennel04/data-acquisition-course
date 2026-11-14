#include <nvs.h>
#include <nvs_flash.h>

// Same four guards as the tested isolated Atom build. initArduino must not
// initialise/auto-erase NVS; display autodetect cannot access its NVS cache.
// No Preferences or saved sensor/credentials/zero namespaces are opened.
extern "C" esp_err_t __wrap_nvs_flash_init() { return ESP_OK; }
extern "C" esp_err_t __wrap_nvs_flash_init_partition(const char*) { return ESP_OK; }
extern "C" esp_err_t __wrap_nvs_open(const char*, nvs_open_mode_t, nvs_handle_t*) {
  return ESP_ERR_NVS_NOT_INITIALIZED;
}
extern "C" esp_err_t __wrap_nvs_open_from_partition(const char*, const char*,
                                                    nvs_open_mode_t, nvs_handle_t*) {
  return ESP_ERR_NVS_NOT_INITIALIZED;
}
