from commands import run

print("For start you can run 'help' command\n")

while True:
  command_value = str(input("\nEnter the command: \n~$/"))

  run(command_value)
  