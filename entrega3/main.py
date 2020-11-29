import pandas as pd
import numpy as np
# Q = Conjunto de estados
# E = Alfabeto
# transitions = Vetor de transições do tipo (estado inicial, caracter, estado final)
# q0 = Estado inicial
# F = Estados Finais

# Recebe um estado, um caracter e o dicionário de transições
# Retorna uma lista dos estados alcançados pelo estado t
def move(T, c, transitions_dictionary):
  # print(T, 'MOVE')
  stack = []
  if (type(T) == list or type(T) == tuple):
    stack = [*T]
  else:
    stack = [T]
  states = []
  while(stack != []):
    # print(stack, 'MOVE STACK')
    state = stack.pop()
    if ((state, c) in transitions_dictionary):
      appendStates = transitions_dictionary[(state, c)]
      states = [*states, *appendStates]

  return tuple(states)

# transitions_dictionary = {
#   (0, None): [1],
#   (1, None): [2, 4],
#   (2, 'b'): [3],
#   (4, 'c'): [5]
# }

# states = move(1, 'b', transitions_dictionary)
# print(states, 'states')

# Recebe um vetor de estados a serem averiguados, o vetor contendo todos os estados do automato e o dicionário de transições
# Retorna uma lista com os estados alcançados a partir de T, usando movimentos vazios (nulos)
def eClosure(T, S, transitions_dictionary):
  stack = [*T]
  closure = []
  while(stack != []):
    t = stack.pop()
    for s in S:
      if(s in move(t, None, transitions_dictionary) and s not in closure):
        closure = [*closure, s]
        stack.append(s)
  closure = [*T, *closure]

  
  return tuple(list(dict.fromkeys(closure))) 

# fecho = eClosure([0, 1, 2], [0, 1, 2, 3, 4, 5], transitions_dictionary)
# print(fecho, 'fecho')

def getTransitionsDictionary(transitions):
  transitions_dictionary = {}
  for transition in transitions:
    data = (transition[0], transition[1])
    if (data in transitions_dictionary):
      transitions_dictionary[data] = [*transitions_dictionary[data], *transition[2]]
    else:
      transitions_dictionary[data] = [*transition[2]]

  return transitions_dictionary

def getUnmarkedState(marked, states):
  for state in states:
    if(state not in marked):
      return state
  
  return None

def convertAutomata(Q, E, transitions, q0, F):
  transitions_dictionary = getTransitionsDictionary(transitions)
  d_table = []
  s0 = eClosure([*q0], Q, transitions_dictionary)
  print(s0, 'S0')
  states = [tuple([*s0])]
  marked = []
  F_ = []
  while(marked != states):
    print(states, 'STATES')
    print(marked, 'MARKED')
    T = getUnmarkedState(marked, states)
    marked = [*marked, T]
    for c in E:
      T_MOVE = move(T, c, transitions_dictionary)
      T_ = eClosure(T_MOVE, Q, transitions_dictionary)
      print(T, 'T')
      print(T_MOVE, 'T_MOVE')
      print(T_, 'T_')
      if T_ not in states and T_ != ():
        states = [*states, tuple(T_)]
        print(states)
      transition = [T, c, T_]
      d_table.append(transition)
  for state in states:
    for s in state:
      if (s in F):
        F_.append(state)

  return tuple([states, E, d_table, s0, F_])


def writeCSV(data, path):
  pd.DataFrame(data).to_csv(path, header=False, index=False)

def getTransitions(transitions_csv):
  transitions = []
  for transition in transitions_csv:
    origin_state = int(transition[0])
    character = None
    if transition[1] != 'None':
      character = transition[1]
    destiny_states = []
    destiny_transitions = transition[2].split(',')
    for state in destiny_transitions:
        new_state = int(state)
        destiny_states.append(new_state)
    data = [origin_state, character, destiny_states]
    print(data, 'data')
    transitions.append(data)

  return transitions

def getAlphabet():
  # E = [
  #   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ç',
  #   'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ç',
  #   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  #   '_', '-', '\'', '"',
  #   ' ', '\t', '\n',
  #   '=', '-', '*', '+', '/',
  #   ':', '>', '<',
  #   ',', ';', '(', ')', '{', '}', '[', ']',
  #   'digito',
  #   'letra',
  #   'outro ^ [letra digito]',
  #   'outro ^ [None . digito]',
  #   'outro ^ [None digito]',
  #   'outro ^ [" " \t \n]',
  #   'outro ^ [= >]',
  # ]
  E = ['a', 'b']

  return E

def getNFAFromCSV(transitionsCSV):
  states = np.arange(0, 11)
  transitions_df = pd.read_csv(transitionsCSV, delimiter=',', header=None)
  transitions_data = transitions_df.values
  transitions = getTransitions(transitions_data)
  initial_state = [0]
  E = getAlphabet()
  F = [10]

  return (states, E, transitions, initial_state, F)      

nfa = getNFAFromCSV('teste_transicoes.csv')
dfa = convertAutomata(nfa[0], nfa[1], nfa[2], nfa[3], nfa[4])
dfa_transitions = dfa[2]
writeCSV(dfa_transitions, 'transitions.data')