/*
   Rodent Treadmill for Awake/Behaving Multi-photon Imaging
*/

const int stp = 2;
const int dir = 3;
const int MS1 = 4;
const int MS2 = 5;
const int MS3 = 6;
const int EN = 7;

String user_input;
float delayDuration = 10.0;
int userSpeed = 1;

void setup() {
  pinMode(stp, OUTPUT); digitalWrite(stp, LOW);
  pinMode(dir, OUTPUT); digitalWrite(dir, LOW);
  pinMode(MS1, OUTPUT); digitalWrite(MS1, LOW);
  pinMode(MS2, OUTPUT); digitalWrite(MS2, LOW);
  pinMode(MS3, OUTPUT); digitalWrite(MS3, LOW);
  pinMode(EN, OUTPUT); digitalWrite(EN, HIGH);
  resetBEDPins();

  Serial.begin(115200);

  Serial.println("Type 'g' to begin.");
  Serial.println();
  while (true) {
    if (Serial.available()) {
      while (Serial.available()) {
        char c = Serial.read();
        user_input += c;
        delay(5);
      }
      if (user_input == "g") {
        digitalWrite(EN, LOW);
        Serial.println("Beginning program at Speed = 1 (Delay = 10 ms).");
        Serial.println();
        Serial.println("Input value (1-100) to change stepper speed.");
        Serial.println("Type 's' to terminate program.");
        Serial.println();
        break;
      }
      else {
        Serial.println("Invalid input. Please try again.");
        Serial.println();
      }
    }
  }
}

void loop() {
  if (Serial.available()) {
    user_input = "";
    while (Serial.available()) {
      char c = Serial.read();
      if (c != 's' && !isDigit(c)) {
        Serial.println("Unrecognized character. Retaining current speed setting.");
        Serial.println();
        while (Serial.available()) {
          c = Serial.read();
          delay(5);
        }
        user_input = String(userSpeed);
        break;
      }
      user_input += c;
      delay(5);
    }
    if (user_input == "s") stepperHalt();
    else {
      userSpeed = user_input.toInt();
      int userSpeedMapped = map(userSpeed, 1, 100, 0, 90);
      //Serial.print("Mapped value: ");
      //Serial.println(userSpeedMapped);
      delayDuration = 10.0 - ((float)userSpeedMapped / 10.0);
      Serial.print("Speed = ");
      Serial.print(userSpeed);
      Serial.print(" (Delay = ");
      Serial.print(delayDuration);
      Serial.println(" ms).");
      Serial.println();
    }
  }
  else {
    digitalWrite(stp, HIGH);
    delay(delayDuration);
    digitalWrite(stp, LOW);
    delay(delayDuration);
  }
}

void stepperHalt() {
  resetBEDPins();
  Serial.println("Program terminated.");
  while (true) {
    ;
  }
}

void resetBEDPins() {
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
  digitalWrite(EN, HIGH);
}
