# UW CSE HW Scraper
For people who want to test their code for CSE homeworks, but are annoyed by the fact that they need to type in the input manually to test their work.

I mean, computers are supposed to make our lives easier, right? So why does UW CS want us to type in stuff *manually*?

So solution: make the manual work automated. This scraper gets the expected outputs from the cse hw diff tool and compiles them into one big out file. It also parses the expected inputs (you know, the ones that you'd 'normally' type) and puts them in a seperate file, with one test case per line.

just run this python script anywhere, and it'll make these files in the same directory.

It's pretty easy to change the `whatevermain.java` programs to read from a file instead of from the console. I'll use Assassin as an example:

```
public class AssassinMain {
    public static void main(String[] args) throws FileNotFoundException {
        // prompt for file name
        Scanner console = new Scanner(System.in);
        System.out.println("Welcome to the CSE143 Assassin Manager");
        System.out.println();
        System.out.print("What name file do you want to use this time? ");
        String fileName = console.nextLine();

        // read names into a list, using a Set to avoid duplicates
        Scanner input = new Scanner(new File(fileName));
        Set<String> names = new TreeSet<String>(String.CASE_INSENSITIVE_ORDER);
        List<String> names2 = new ArrayList<String>();
        while (input.hasNextLine()) {
            String name = input.nextLine().trim();
            if (name.length() > 0 && !names.contains(name)) {
                names.add(name);
                names2.add(name);
            }
        }

        // shuffle if desired
        if (yesTo(console, "Do you want the names shuffled?")) {
            Collections.shuffle(names2);
        }
        // make an immutable version and use it to build an AssassinManager
        List<String> names3 = Collections.unmodifiableList(names2);
        AssassinManager manager = new AssassinManager(names3);
        System.out.println();

        // prompt the user for victims until the game is over
        while (!manager.gameOver()) {
            oneKill(console, manager);
        }

        // report who won
        System.out.println("Game was won by " + manager.winner());
        System.out.println("Final graveyard is as follows:");
        manager.printGraveyard();
    }
    .
    .
    .
```
The first thing we need to do is read from the file instead of from console. We can make a new Scanner to do that.
`Scanner input = new Scanner("path_to_input_file");`
Since each test case is one line, we need to run the code in the main method a bunch of times. So we'll wrap the main method in a loop.
```
public class AssassinMain {
    public static void main(String[] args) throws FileNotFoundException {
        Scanner input = new Scanner("path_to_input_file");
        while(input.hasNextLine()){
            // prompt for file name
            Scanner console = new Scanner(System.in);
            System.out.println("Welcome to the CSE143 Assassin Manager");
            System.out.println();
            .
            .
            more main code
            .
            .
            System.out.println("Game was won by " + manager.winner());
            System.out.println("Final graveyard is as follows:");
            manager.printGraveyard();
        }
    }
    .
    .
    .
```
now we can replace `Scanner console = new Scanner(System.in)`

with `Scanner console = new Scanner(input.nextLine());`

This shouldn't break any of the code, everything should still compile. However, we do need to add one more thing, and that is extra print statements. Before, you typed in the input and pressed enter. So now we have to tell the computer to do the same thing.

basically, look in the code for whenever the main function asks for input, and add a println statement after that. Here's an example:
```
System.out.print("What length word do you want to use? ");
int length = console.nextInt();
>>System.out.println(length);<< add this
```
the last line is what needs to be added for stuff to work. You shouldn't need to delete any lines, just make sure you do this *right after* the `console.nextwhatever` line.

one more thing... if your inputs look wrong, it's probably because you need to delete some of the data from the input file. Sometimes the scraper data looks like this:
```
  log 1: dictionary2.txt, SHOW_COUNT=true  4  7  e  o  t  f  c  n  d  h  g
  log 2: dictionary2.txt, SHOW_COUNT=true  4  7  l  h  e  o  f  c  g  d
  log 3: dictionary2.txt, SHOW_COUNT=true  4  8  u  t  o  e  w  f  x  r  b  i
  log 4: dictionary.txt, SHOW_COUNT=true  8  14  a  o  i  u  e  t  m  n  p  s  r  l  b  c  h  d  j  w
  log 5: dictionary.txt, SHOW_COUNT=false  5  10  o  e  i  a  u  y  g  t  n  s  l  m
  log 6: dictionary.txt, SHOW_COUNT=false  6  12  a  e  i  o  u  y  g  n  t  r  s  l  p  m  b
  log 7: dictionary.txt, SHOW_COUNT=false  4  15  o  u  e  i  a  t  l  r  s  m  n  b  c  p  d  g  f
  log 8: dictionary.txt, SHOW_COUNT=false  10  15  e  o  a  i  u  y  t  g  n  l  h  m  p  r  s  w
  log 9: dictionary.txt, SHOW_COUNT=false  23  42
```
you can delete the log 1: stuff or any of the other useless data that comes in from the scraper. Just make sure you don't delete something important for the test case!

if you run your main, you'll basically get the output of each of the test cases in sequential order. You can paste that output into a new file and compare it to the `out_HW[X] ([Assignment_Name]).txt` file made by the scraper. One easy way to compare files is to use the diff command in a terminal window (works on MacOS and linux). The syntax is `diff path-to-file-1 path-to-file-2`.
For windows you can use `fc path-to-file-1 path-to-file-2` in Windows Command Prompt.


Have a problem? Make an issue!
