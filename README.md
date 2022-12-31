# MIDI to Guitar tabs
Converts a MIDI file to ASCII guitar tabs.

## Using the tool

First, clone the repo.

Then, place your midi files in the *midis* folder.

To convert the midis to tabs, make sure the repo is the working directory and use the command : `python midi_tabs.py yourmidifile.mid` in the terminal.

You should find the generated tabs in the *tabs* folder.

## Expected results

This is the kind of result you are expecting to get :

```text
E ||----------3----3----|5----5----3--------|1----1----0----0----|-------------------|3----3----1----1----|0----0-------------|3----3----1----1----|0----0-------------|----------3----3----|5----5----3--------|1----1----0----0----|-------------------|
B ||1----1----1---------|-------------------|--------------------|3----3-------------|--------------------|----------3--------|1-------------------|----------3--------|1----1----1---------|-------------------|--------------------|3----3-------------|
G ||--------------------|5---------5--------|2---------0---------|0---------5--------|5---------2---------|0---------0--------|----------2---------|0---------0--------|--------------------|5---------5--------|2---------0---------|0---------5--------|
D ||2-------------------|-------------------|--------------------|----------2--------|--------------------|-------------------|--------------------|-------------------|2-------------------|-------------------|--------------------|----------2--------|
A ||3---------3---------|----------3--------|----------3---------|----------3--------|3-------------------|-------------------|3-------------------|-------------------|3---------3---------|----------3--------|----------3---------|----------3--------|
E ||--------------------|1------------------|1-------------------|3------------------|----------1---------|3---------3--------|----------1---------|3---------3--------|--------------------|1------------------|1-------------------|3------------------|

```
 This is the generated tab for a twinkle twinkle little star midi.
 
## Limitations
The generated tabs are often different from how a human would play.

Also, the tool can't handle complicated multi-channel MIDI files, but it's not what it's made for.

# Behind the tool

## Glossary

Fingering : Finger positions used by a guitar player to play a note or multiple notes.

Chord : Multiple notes played simultaneously.

## Why the problem is interesting 

The problem of generating guitar tablatures is not trivial because a single note can be played at multiple distinct positions on a guitar. Pressing a different fret on a different string can generate a sound that has the same frequency. A tablature essentially dictates the player the best finger positions to use to play a sequence of notes.
The problem would be easy if a note could only be played on one position, it would be enough just to indicate the notes one by one and there would be no ambiguity on the way to play them, but it's not that simple.

For example, you must take into account the notes played before to choose the finger positions that will minimize the difficulty of transitioning between two fingerings for the player. Typically, the positions must be as close to each other as possible.
Another example : if you want to play a chord - multiple notes simultaneously - there are dozens of combinations of possible fingerings to play that chord. You want to find the optimal fingerings to play these chords.
This problem is referred to as the fingering problem.

*All the possible fingerings to play a C :*
![All the possible fingerings to play a C](https://i.imgur.com/6WWheRR.png)

## How it works

The sequence of notes and fingerings is modeled as a Hidden Markov Model (HMM), with the fingerings being the hidden states and the notes being the observed states.

Our goal is to predict the most likely sequence of hidden states using the sequence of observed states.

To find that sequence, we can make use of the Viterbi algorithm. This algorithm outputs the most likely sequence of hidden states using the sequence of observed states, the transition probabilities and the emission probabilities of the model.

Transition probabilities are the probabilities to go from one hidden state to some other hidden state. In our case, it's the probability to transition from a fingering to some other one.

Emission probabilities are the probabilities to get an observed state given a hidden state. In our case, it can be seen as the probability that a certain set of notes will be heard given a certain fingering. 

These probabilities are stored in a transition matrix and an emission matrix.
To build these matrices, we first explore the MIDI file chronologically. For each note or chord that we encounter in the file, we will compute all the fingerings that will produce these notes.

The guitar fretboard is modeled as a complete graph, in the graph theory sense. The nodes correspond to the frets of for each string and the edges represent the distance between the nodes. Being a complete graph, all the nodes are connected by an edge to each other.
This graph is what enables us to find all the ways that a set of notes can be played, using a simple depth-first search algorithm.

In order to compute the transition probabilities between the fingerings, we use a difficulty metric that is defined as :



