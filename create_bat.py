with open("exec2.bat", mode="w") as f:
    f.write("set name=%1\n")
    f.write("type null > %name%.txt\n")
    for i in range(1000):
        f.write(f"tools\\vis.exe in\\{i:04}.txt out\\{i:04}.txt >> %name%.txt 2>&1\n")
