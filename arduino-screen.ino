#include <Wire.h>
#include <LiquidCrystal_I2C.h>


String processSpecialChars(String text);

LiquidCrystal_I2C lcd(0x27, 16, 2);
const int LCD_WIDTH = 16;

void setup() {
  Serial.begin(9600);

  // Prepare the screen
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("  Disconnected  ");

  // Send a ready signal
  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();

    // Clear screen before new message
    lcd.clear();

    String processedMsg = processSpecialChars(msg);

    if (processedMsg.length() > LCD_WIDTH) {
      // First line
      lcd.setCursor(0, 0);
      lcd.print(processedMsg.substring(0, LCD_WIDTH));
      // Second line
      lcd.setCursor(0, 1);
      lcd.print(processedMsg.substring(LCD_WIDTH));
    } else {
      // Short message
      lcd.setCursor(0, 0);
      lcd.print(processedMsg);
    }
    } 
  }
  

// Correct display of the degree sign
String processSpecialChars(String text) {
  String processedText = "";
  char lastChar = 0;

  for (int i = 0; i < text.length(); i++) {
    char currentChar = text.charAt(i);

    /*
      Checks the previous and current character to determine if there should
      be a degree sign at that position (due to Python's encoding).
    */
    if ((byte)lastChar == 0xC2 && (byte)currentChar == 0xB0) {
      processedText += (char)223; // Add degree symbol
      lastChar = 0; // Reset previous character
    } else {
      if ((byte)currentChar != 0xC2 && (byte)currentChar != 0xC3 && (byte)currentChar != 0xC4 && (byte)currentChar != 0xC5) {
        processedText += currentChar;
      }
      lastChar = currentChar;
    }
  }
  return processedText;
}