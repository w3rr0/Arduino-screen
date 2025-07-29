#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// adres I2C (najczęściej 0x27 lub 0x3F), szerokość 16, wysokość 2
LiquidCrystal_I2C lcd(0x27, 16, 2);
const int LCD_WIDTH = 16;

void setup() {
  Serial.begin(9600);

  lcd.init();              // Inicjalizacja LCD
  lcd.backlight();         // Włączenie podświetlenia
  lcd.setCursor(0, 0);     // Ustaw kursor na początku pierwszej linii
  lcd.print("  Disconnected  ");

  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();

    // Wyczyść ekran przed wyświetleniem nowej wiadomości
    lcd.clear();

    if (msg.length() > LCD_WIDTH) {
      // Pobierz pierwszą część wiadomości (16 znaków)
      String firstLine = msg.substring(0, LCD_WIDTH);
      
      // Pobierz resztę wiadomości
      String secondLine = msg.substring(LCD_WIDTH);

      // Wyświetl pierwszą część na górnej linijce
      lcd.setCursor(0, 0);
      lcd.print(firstLine);

      // Wyświetl drugą część na dolnej linijce
      lcd.setCursor(0, 1);
      lcd.print(secondLine);

    } else {
      // Jeśli wiadomość jest krótka, wyświetl ją normalnie
      lcd.setCursor(0, 0);
      lcd.print(msg);
    } 
  }
}