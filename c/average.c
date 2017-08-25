#include <stdio.h>
#include <math.h>

int main(int argc, char* argv[]){
  int i = 0, sum = 0, n = 0,avg = 0;
  FILE *fin;

  // Open file
  fin = fopen("testdata29", "r");
  
  // Keep reading in integers (which are placed into "n") until end of file (EOF)
  while(fscanf(fin, "%d", &n) != EOF){
      // Add number to sum
      sum += n;

      // Increment counter for number of numbers read
      i++;

      // Average is sum of numbers divided by numbers read
      avg = (sum / i);
  }

  // After the loop is done, show the average
  printf("The average is %d.\n", avg);

  fclose(fin);
  return 0;
}
