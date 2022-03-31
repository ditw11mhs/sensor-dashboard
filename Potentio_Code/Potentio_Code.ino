const int pot1 = 4;
const int pot2 = 2;
const int pot3 = 15;

int pot1_val = 0;
int pot2_val = 0;
int pot3_val = 0;

float bit_to_volt(float bit_data){
  return bit_data/4095*3.3;
  }

void setup() {
  pinMode(pot1,INPUT);
  pinMode(pot2,INPUT);
  pinMode(pot3,INPUT);
  Serial.begin(9600);
}

void loop() {
  pot1_val = analogRead(pot1);
  pot2_val = analogRead(pot2);
  pot3_val = analogRead(pot3);

  Serial.print(bit_to_volt(float(pot1_val)));
  Serial.print("|");
  Serial.print(bit_to_volt(float(pot2_val)));
  Serial.print("|");
  Serial.println(bit_to_volt(float(pot3_val)));
  delay(10);
}
