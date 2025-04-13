export KIVY_METRICS_DENSITY=1
export KIVY_BCM_DISPMANX_ID=2
export KIVY_GL_BACKEND=kivy.core.window.window_sdl2
export SDL_VIDEODRIVER=kmsdrm

sudo ip link set can0 up type can bitrate 500000