#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

String in;

void setup() {
  lcd.init();
  lcd.backlight();


  Serial.begin(9600);
  Serial.setTimeout(3);
}

void loop() {    
  lcd.clear();
  Serial.println(1);
  lcd.print("Connected");
  while(!Serial.available());
  lcd.clear();
  in = Serial.readString();
  if (in == "quit"){
    lcd.clear();
    lcd.noBacklight();
    lcd.off();
    while(!Serial.available());
    lcd.backlight();
    lcd.on();
  }

  lcd.setCursor(0, 0);
  Serial.println(0);
  Serial.println("Song: " + in);
  int inLen = in.length();

  if(inLen <= 16){
    lcd.print(in);
    delay(8000);
  } else if(inLen <= 32){
    for (int Char = 0; in[Char]; Char++){
      lcd.print(in[Char]);
      if(Char == 15){
        if(in[Char] == ' '){
          lcd.setCursor(-1, 1);
        } else {
          lcd.setCursor(0, 1);
        }
        
      }
    }
    delay(8000);
  }else {
    lcd.setCursor(15, 0);

    for (int thisChar = 0; in[thisChar]; thisChar++){
      lcd.print(in[thisChar]);
      delay(400);
      lcd.scrollDisplayLeft();
    }
    for(int x = 0; in[x]; x++){
      lcd.scrollDisplayRight();
    }
  }
}