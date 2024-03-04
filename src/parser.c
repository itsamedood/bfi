#include <stdio.h>
// #include <stdlib.h>
#include <string.h>
#include "parser.h"

void parseBfCode(char *code)
{
  int data[30000];
  int pointer = 0;
  int loopStart = 0;

  int i = 0;
  int j = 0;

  while (i < strlen(code) && j < MAX_ITER)
  {
    char c = code[i];

    switch (c)
    {
      case '>':
        pointer++;
        break;

      case '<':
        pointer--;
        break;

      case '.':
        printf("%c", (char)data[pointer]);
        break;

      case ',':
        int inputNum = NULL;
        while (inputNum == NULL)
        {
          printf("📥 ");
          scanf("%i", &inputNum);

          printf("%i (%c)\n", inputNum, (char)inputNum);
        }

        break;

      case '+':
        data[pointer]++;
        break;

      case '-':
        data[pointer]--;
        break;

      case '[':
        loopStart = i;
        break;

      case ']':
        if (data[pointer] != 0) i = loopStart;
        break;
    }
  }
}
