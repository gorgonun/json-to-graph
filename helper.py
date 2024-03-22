def main():
    with open("result.txt") as f:
        for line in f.readlines():
            splitted_line = line.split(" ")
            if splitted_line[3] == "RUN":
                print(" ".join(splitted_line[4:]).replace("\\n", "\n"))


if __name__ == "__main__":
    main()
