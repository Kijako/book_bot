import re

def Create_Pattern():
  patternDict = [
        {
      #'pattern' :r'(?i).*(description|describe|tell me).+\s+(about|of|in)\s+(.+)\s+\?', 
          
      #changé pour catch '.' et '?', par contre, il faut écrire uniquement selon l'orthographe anglaise, pas d'espace entre le mot et le '.' ou le '?'
      
      #Tell me (more) about the LOTR ?
      'pattern' :r'(?i).*(description|describe|tell me|tell me more)\s+(about|of|in)\s+(.+)\W',
      'intent':"Description"
    },

    {#who wrote the LOTR?
     # I wanna know who is the author of the LOTR.
     'pattern' :r'(?i).*(author of|wrote)\s+(.+)\W',
     'intent':"Author"
    },

    {# I'd like to know how many pages are there in the LOTR.
     # Please, what is the length of the LOTR?
     #(?i).*(long|length|pages)\s+.+(is|of|in)\s+(.+)
     # (?i).*(long|length|pages)(.*?)\b(in|of|is)\b(.*)\W
     'pattern' :r'(?i).*(long|length|pages)(.*?)\b(in|of|is)\b\s(.*)\W',
     'intent':"Length"
    },

    {# tell me what is the price of the LOTR.
     #could you tell me How much is the LOTR?
     'pattern' :r'(?i).*(price|how much)\s+(about|of|in|is)\s+(.+)\W',
     'intent':"Price"
    },
    
    
    {# Basic greetengs : hello; hi !; hey!
     'pattern': r'(?i)\b(Hi|Hello|Hey|hello|hi)\b',
     'intent': 'Hello'
    }, 
    
    {# Basic goodbye
     #'pattern': r'/\b(bye|exit|quit|leave|stop)\b/i',
      'pattern': r'(?i)\b(bye|exit|quit|leave|stop)\b',
      'intent': 'Exit'
    },
    
    {
     # 'pattern': r'/\b(help)\b/i',
      'pattern': r'(?i)\b(help)\b',
      'intent': "Help"
    },

    {
      'pattern': r'(?i)^yes$',
      'intent': "Yes"
    }, 

    {
      'pattern': r'(?i)^no$',
      'intent': "No"
    },

    {
      'pattern': r'(?i)^Recommendation$',
      'intent': "Recommendation"
    }
  
  
  ]
  return patternDict



def searchPattern(patternDict, exp):
  for p in patternDict:
    # print(p['pattern'])
    # print(exp)
    # print(re.match(p['pattern'],exp))
    if re.match(p['pattern'],exp):
      result = re.search(p['pattern'],exp)
      print(result.groups())
      return [p['intent'], list(result.groups())]
  return ('No_Match', 0)