# human
## Quickstart:
1. Clone this repository.
2. Install python 3.9.6 (earlier versions may also work).
3. In terminal, navigate to the /human directory and execute 'python human.py programs/setup.human'
4. Follow the instructions. That's it!

## Introduction

Hello! This is the interpreter for the language 'human' (also known as 'humanlang'), which is a simple language for human programming. Human relies on the capabilities of existing natural languages to create meaningful imperative commands.

The real power of human is in the creativity of the human executing the program. Because of this creativity, a very simple human program can conceivably bootstrap itself into a very complex and powerful one, as long as the program instructs the human to iteratively improve the program itself.

Here are silly example .human files:
```
# blend.human  
HOW TO blend {something} until smooth using a blender:  
press the button the says 'blend' on your blender.  
watch {something} until no chunks appear.  
press the 'off' button to turn the blender off.  
```
```
# smoothie.human  
HOW TO make a {special ingredient} flavored smoothie:  
put the {special ingredient} and frozen fruit in your blender until the blender is half full.  
FOLLOWING ./blend.human: blend [the fruit and {special ingredient}] until smooth.  
pour the contents of the blender into a large glass.  
```

## The human language:
### Comments
Anything after a '#' is considered a comment and removed from the line. To write a '#' and not have it act as a comment, escape it with a backslack '\\#'.
### Files
A .human file is a single executable program for humans. Each file starts with a *goal line*, then has one or more *instruction lines*.
#### Goal line
A .human file MUST start with a goal of the form 'HOW TO [insert goal]'. Note that the goal is only the part *after* 'HOW TO'. It is okay lines above the goal if they only include comments and line breaks.
#### Instruction lines
After the goal, all lines are instructions. An instruction is a single atomic thing for a human to do. The instructions in a file, when followed in sequence, should produce the result described in the file's goal line.
### Variables
The goal may contain variables, which are textual symbols wrapped in curly braces. (Example: 'HOW TO send {friend's name} a message'). When a variable's value is set, all other instances of the variable in the file are replaced with that value.
### Sub-instructions
An instruction that begins with 'FOLLOWING ' will load the instructions for another .human file, and deliver them in sequence. For the nerdy, you can think of this as creating a new stack frame of human instructions.  
After 'FOLLOWING ', write the relative or absolute filepath, then a colon or space, then the goal of the program being called, with variables inserted in brackets.
Syntax example: `FOLLOWING ./blend.human: blend [a piece of fruit] until smooth.  `  
That line will call the file blend.human, setting the single variable to have value 'a piece of fruit'.

## Usage
Add a command line argument after `python human.py` to specify which `.human` file to run.  
Optionally, also add the `--values` argument, after which you may list variable values in the same order that those variables were found in the goal. If a program has variables, you must specify them.  
### Example:
Say we have the following file:
```
# foo.human
HOW TO do say {one thing} and then {another}
say {one thing}
finally, say {another}
```
In order to run the program 'foo.human', we must specify both variables (`{one thing}` and `{another}`). If we would like the first of the two variables (`{one thing}`) to have value 'bar' and the second variable (`another`) to have value 'foo bar', we run the following line: `python human.py foo.human --values "bar" "foo bar"`.  
This would yield the following instructions:  
`DO THIS: say foo`  
and:  
`DO THIS: finally, say foo bar`

## How to be an effective human programmer
### Use your future self's creativity
Your future self is pretty smart -- maybe even smarter than you are today! Use your future self, and their information about the world, to make better programs:
```
# future.human
HOW TO plan your day and update your planning program
FOLLOWING ./plan.human, plan my day
set a reminder for tonight to "Analyze how my plan went and make changes to plan.human accordingly"
```
### Make infinite loops, but make sure they have breakout mechanisms
Infinite loops are a powerful tool for human programs, but they can easily become impossible or detrimental. As a rule of thumb, any infinite loop should have a breakout mechanism.  
Here's a bad breakout mechanism: `if you would like to break out of this infinite loop, delete the step that restarts the program`. This mechanism is bad because it lets the user break out for no reason.  
Here's a slightly better one: `when you have satisfactorily completed the goal of this program, delete the instruction that restarts the program`.  This ensures that the user only breaks out after the program has worked its magic.  
Even better, make the breakout mechanism implicit in a *creative improvement* instruction like the following: `Edit this program so that it's more likely to cause you to reach your goal`. This instruction implicitly allows you to remove the looping instruction *if it is no longer helping you reach your goal*. The benefit of a creative improvement instruction like this is that it also allows your program to naturally evolve through time to fit your needs.
```
# happy.human
HOW TO make people happy                                                      # clear and difficult goal
Edit this program so that it's more likely to cause you to make people happy  # creative improvement
Set a reminder for tomorrow to run happy.human                                # infinite recursion
```

### Comply
#### To be an effective human programmer, you must comply with every instruction of every program you run.  
Compliance does much more than just help you get things done: knowing you will be 100% compliant __drastically__ expands the space of possible program outcomes, and thereby drastically increases your abilities as a programmer. Consider the program happy.human above: this program is short, and may seem simple, but it is theoretically very complicated. To comply with this program, you must perform more than just the two lines of instructions: you must perform the instructions the next day, and the next, and so on, while each day the program may evolve. Even a short human program can be very complex, and the best programs *are* very complex!  

Missing a single day, or a single instruction, could jeopardize the success of this program. And as a programmer, knowing that you might not comply with all instructions of any program you write is incredibly limiting.

#### With great compliance comes great responsibility.
A wise human programmer knows to be responsible with their programs, ensuring that each program is *clear*, *doable*, and *beneficial*.  
**Clear** -- Clear programs are easier to complete, and easier to evaluate before running. Often, complex tasks can be broken into more specific sub-tasks for greater clarity.  
**Doable** -- Good programs are not just doable, they have have absolutely no possibility of unintentional failure. Common causes of failure include hard tasks, tasks with deadlines, and infinite loops with no breakout mechanism.  
**Beneficial** -- You need to think carefully about whether a program is beneficial to you *before* you run it, otherwise you are stuck with a bad decision between non-compliance and self detriment.

#### As a last resort, throw a *very-specific* error
You want to be 100% compliant, but you need a backup plan in case you come across a program that's impossible or detrimental. In that case, you can "throw an error", much like a computer does when it can't complete an instruction. To throw an error, just say to yourself why you are not complying, and close the program. However, understand that every error you throw opens up the possibility for similar non-compliance in the future, and thus weakens your ability as a programmer.  

examples of good errors:  
* Error: I didn't understand the instruction
* Error: caught in an infinite loop with no breakout mechanism
* Error: had to save someone's life instead of performing the instruction

The errors above are good because as a programmer, I don't care that the user (me) can throw these errors: I don't want myself to push through instructions I don't understand, or get stuck in an infinite loop forever.  

examples of bad errors:
* Error: I realized I don't want to do this anymore
* Error: I'm too tired to do this
* Error: plans conflicted with this program

The errors above are bad because they *do* significantly limit the programmer. How do you write an effective program if your subject might get tired or bored at any minute and skip a line or close the program?  

It may be smart to keep an **error log** where you record your errors and their causes. This will help you program in such a way that limits similar errors being thrown in the future. Remember: the goal is to have zero errors in the first place.

## Next steps
Humanlang will be the precursor for an agent-oriented language (or maybe just a human-centric agent library to plug into existing agent-oriented languages). The vision is roughly like this:

```
# dotasks.txt
Computer: set user_productivity_settings to no_distractions_1
Computer: open todolist.txt in sublime text
Human: rearrange the list in ascending priority until it's ready to be reviewed by {friend's name}.
Computer: save todolist.txt
Computer: close todolist.txt
Computer: send todolist.txt over email to {friend's name}
Computer: set user_productivity_settings to receive_pending_notifications
Human: Review all notifications and collect notifications you need to respond to in {notification doc}
Computer: set user_productivity_settings to no_distractions_1
Human: close you computer, go outside, and meditate for 20 minutes
```

...and so on. The computer language would be more structured, but the idea is that shared instructions between humans and computers could be really powerful, especially if the instructions become self-referrential.
