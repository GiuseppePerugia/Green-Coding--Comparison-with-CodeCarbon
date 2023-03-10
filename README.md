# Green-Coding--Comparison-with-CodeCarbon

This code aim to show difference in energy consumption between two similar solitaire applications.

Note: This guide will refer to the non-energy efficient code with code1 and to the energy efficient code as code2. 
      code1 will be solitaire.py while code2 will be solitaire-Improved.py

## Requirements

To analyse the carbon emissions the application makes use of CodeCarbon.

To install CodeCarbon simply run:
> pip install codecarbon

To have more information about CodeCarbon navigate to the repository: https://github.com/mlco2/codecarbon

To install all the necessary requirements run:
> pip install -r requirements.txt

Make sure to be in the repository directory to run the command.

## Graphic Visualization

CodeCarbon produce a csv emissions file with all detailed informations regarding the emissions of the code.

To have a visualization of those information run the following command:
> carbonboard --filepath="examples/emissions.csv" --port=8050

If the default port 8050 it's occupied, use another port (such as 3333).

The command will produce an host link to show the visualization of the emissions.

Example:
![image](https://user-images.githubusercontent.com/89920701/224378880-fb3f0081-2b58-497a-b771-390f5c38a33d.png)

# Code Analysis

In the following you can find bad and good practices of the codes provided.

## Eliminate unnecessary operations

In code1 a series of useless else are scattered through the code causing dealys and multiple print statements.
In code2 does not happens reducing the computational workload.

## Avoiding unnecessary functions calls

In code1 we call same functions multiple times which requires power and energy to access them.
We can simply call a function once, store it in a variable and use that variable when you need the function.
We save energy and the code looks more tidy.

## Avoid unnecessary variables

Unnecessary variables have been placed at the  beginning of code1.
These variables stores cards values, colours, and  symbols.
In code2 this does not happens and the cards values, colours, and symbols are simply added to a list.
Although this does not have an huge impact due to the low numbers of elements in the deck, the power consumption would grow in case of a bigger deck of  cards.

## Use appropriate algorithms

In code1 we’re using a bogo sort to list our cards left in the deck.
In code2 we’re implementing a merge sort.
It’s well known that a merge sort and quick sort are the most efficient sort methods to save energy and resources.

## Use language specific features

Using proper comprehensive lists  to avoid useless methods to list the cards.
In code1 we’re using 1 for loop with 2 nested for loops  to list the cards while in code2 we  use a comprehensive list, which is makes spare an enormous amounts of energy.

## Avoiding using global variables

In code1 we have a global variable declared which is used in different methods.
This can occupy excessive memory unnecessarely.
In code2 this does not happens. This because the functions should be defined aspure components as far as possible.

## Libraries
Labriaries are very beneficial as they help to implement functionalities faster compared to write code from scratch.
In code2 we use itertool library to achieve a better comprehensive listing of our cards.

# Known Issues
The cards are sorted in ASCII code. This means that the 10s will be placed as first since 1 comes first in ASCII than 2.
This also happens to the K which comes after the J but before the Q.
