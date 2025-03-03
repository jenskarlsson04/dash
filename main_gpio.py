from GPIO_reader import subscribe_gpio_pint, btn_screen

def run():

    print("GPIO triggered")

subscribe_gpio_pint(btn_screen, run)


if __name__ == "__main__":
    while True:
        pass
