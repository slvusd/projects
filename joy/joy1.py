import pygame

pygame.init()
pygame.joystick.init()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Joystick button {event.button} pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print(f"Joystick button {event.button} released.")
        if event.type == pygame.JOYAXISMOTION:
            print(f"Joystick axis {event.axis} value: {joystick.get_axis(event.axis)}")
        if event.type == pygame.JOYHATMOTION:
            print(f"Joystick hat {event.hat} value: {joystick.get_hat(event.hat)}")

    # Print all joystick values
    for i in range(joystick.get_numaxes()):
        print(f"Axis {i} value: {joystick.get_axis(i)}")
    for i in range(joystick.get_numbuttons()):
        print(f"Button {i} value: {joystick.get_button(i)}")
    for i in range(joystick.get_numhats()):
        print(f"Hat {i} value: {joystick.get_hat(i)}")

    pygame.time.wait(100)  # Wait for 100 milliseconds

pygame.quit()

