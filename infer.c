#include<stdio.h>
#include<string.h>
#include<math.h>
int main()
{
    int answer[10];
    int b[10];
    int count[4];
    int i;
    int j;
    int k=0;
    int max, min;
    max=0;
    int max_order = 0;
    min=10;
    int min_order = 0;
    char test='A';
    for(i=0;i<10; i++){
        answer[i] = 0;
        b[i]=0;
        count[i]=0;
    }
    printf("test\n");

    for(b[0]=0; b[0]<4; b[0]++){
        for(b[1]=0; b[1]<4; b[1]++){
            for(b[2]=0; b[2]<4; b[2]++){
                for(b[3]=0; b[3]<4; b[3]++){
                    for(b[4]=0; b[4]<4; b[4]++){
                        for(b[5]=0; b[5]<4; b[5]++){
                            for(b[6]=0; b[6]<4; b[6]++){
                                for(b[7]=0; b[7]<4; b[7]++){
                                    for(b[8]=0; b[8]<4; b[8]++){
                                        for(b[9]=0; b[9]<4; b[9]++){
                                            if(b[1]<2){ if(b[4]!=(b[1]+2)) continue;}
                                            else {if(b[4]!=(b[1]-2)) continue;}

                                            if(b[2]==0){
                                                if((b[5]!=b[1]) || (b[1]!=b[3]) ||(b[5]!=b[3])|| (b[2]==b[5]) || (b[2]==b[1] ) || (b[2]==b[3]) ) continue;
                                            }else if(b[2]==1){
                                                if((b[2]!=b[1]) || (b[1]!=b[3]) ||(b[2]!=b[3])|| (b[2]==b[5]) || (b[5]==b[1] ) || (b[5]==b[3]) ) continue;
                                            } else if(b[2]==2) {
                                                if((b[5]!=b[2]) || (b[5]!=b[3]) ||(b[2]!=b[3])|| (b[2]==b[1]) || (b[5]==b[1] ) || (b[1]==b[3]) ) continue;
                                            } else{
                                                if((b[5]!=b[1]) || (b[1]!=b[2]) ||(b[5]!=b[2])|| (b[3]==b[5]) || (b[3]==b[1] ) || (b[2]==b[3]) ) continue;
                                            }

                                            if(b[3]==0){
                                                if(b[0] != b[4] ) continue;
                                            } else if (b[3]==1){
                                                if(b[1] != b[6] ) continue;
                                            } else if (b[3]==2) {
                                                if(b[0] != b[8] ) continue;
                                            } else {
                                                if(b[5] != b[9] ) continue;
                                            }


                                            if(b[4]==0){
                                                if(b[7] != b[4] ) continue;
                                            } else if (b[4]==1){
                                                if(b[4] != b[3] ) continue;
                                            } else if (b[4]==2) {
                                                if(b[4] != b[8] ) continue;
                                            } else {
                                                if(b[4] != b[6] ) continue;
                                            }


                                            if(b[5]==0){
                                                if((b[7] != b[1]) || (b[7]!=b[3] ) ) continue;
                                            } else if (b[5]==1){
                                                if((b[7] != b[0]) || (b[7]!=b[5] ) ) continue;
                                            } else if (b[5]==2) {
                                                if((b[7] != b[2]) || (b[7]!=b[9] ) ) continue;

                                            } else {
                                                if((b[7] != b[4]) || (b[7]!=b[8] ) ) continue;
                                            }

                                            for(j=0; j<4; j++){
                                                count[j]=0;
                                            }
                                            for(j=0; j<10; j++){
                                                count[b[j]]++;
                                            }

                                            max = 0;
                                            for(j=0;j<4;j++){
                                                if (count[j] > max) {max = count[j]; max_order = j;}
                                            }
                                            min = 10;
                                            for(j=0;j<4;j++){
                                                if (count[j] < min) {min = count[j]; min_order = j;}
                                            }
                                            if(b[6]==0){
                                                if(( min_order != 2)) continue;
                                            } else if (b[6]==1){
                                                if(( min_order != 1)) continue;
                                            } else if (b[6]==2) {
                                                if(( min_order != 0)) continue;
                                            } else {
                                                if(( min_order != 3)) continue;
                                            }

                                            if(b[7]==0){
                                                if(abs((b[6]-b[0]))==1) continue;
                                            } else if (b[7]==1){
                                                if(abs((b[4]-b[0]))==1) continue;
                                            } else if (b[7]==2) {
                                                if(abs((b[1]-b[0]))==1) continue;
                                            } else {
                                                if(abs((b[9]-b[0]))==1) continue;
                                            }

                                            if(b[8]==0){
                                                if((b[0]==b[5]) == (b[4]==b[5]) ) continue;
                                            } else if (b[8]==1){
                                                if((b[0]==b[5]) == (b[4]==b[9]) ) continue;
                                            } else if (b[8]==2) {
                                                if((b[0]==b[5]) == (b[4]==b[1]) ) continue;
                                            } else {
                                                if((b[0]==b[5]) == (b[4]==b[8]) ) continue;
                                            }

                                            if(b[9]==0){
                                                if((max-min)!=3 ) continue;
                                            } else if (b[9]==1){
                                                if((max-min)!=2 ) continue;
                                            } else if (b[9]==2) {
                                                if((max-min)!=4 ) continue;
                                            } else {
                                                if((max-min)!=1 ) continue;
                                            }
                                            //printf("%d, %d, %d , %d ,max %c : %d ;  min %c : %d\n", count[0], count[1], count[2], count[3],max_order+test, max, min_order+test, min );
                                            printf("final answer is :\n");
                                            for(j=0;j<10;j++){
                                                printf("%c ", (char)(b[j]+test));
                                            }
                                            printf("\n");
                                            for(j=0; j<4; j++){
                                                count[j]=0;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
