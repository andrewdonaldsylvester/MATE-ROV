#define P_CH1  8
#define P_CH2  9
#define P_CH3 10
#define P_CH4 11
#define P_CH5 12
#define P_CH6 13

unsigned int ch1;
unsigned int ch2;
unsigned int ch3;
unsigned int ch4;
unsigned int ch5;
unsigned int ch6;

void setup() {
  Serial.begin(115200);

  pinMode(P_CH1, INPUT);
  pinMode(P_CH2, INPUT);
  pinMode(P_CH3, INPUT);
  pinMode(P_CH4, INPUT);
  pinMode(P_CH5, INPUT);
  pinMode(P_CH6, INPUT);
}

void loop() {
  ch1 = pulseIn(P_CH1, HIGH);
  ch2 = pulseIn(P_CH2, HIGH);
  ch3 = pulseIn(P_CH3, HIGH);
  ch4 = pulseIn(P_CH4, HIGH);
  ch5 = pulseIn(P_CH5, HIGH);
  ch6 = pulseIn(P_CH6, HIGH);

  Serial.print(ch1);
  Serial.print("  ");
  Serial.print(ch2);
  Serial.print("  ");
  Serial.print(ch3);
  Serial.print("  ");
  Serial.print(ch4);
  Serial.print("  ");
  Serial.print(ch5);
  Serial.print("  ");
  Serial.println(ch6);
}
