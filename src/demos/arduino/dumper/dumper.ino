#include <Cart.h>
#include <CartDumper.h>
#include <WiringVCS.h>

#define NBYTES 32

void array_to_string(byte array[], unsigned int len, char buffer[])
{
    for (unsigned int i = 0; i < len; i++)
    {
        byte nib1 = (array[i] >> 4) & 0x0F;
        byte nib2 = (array[i] >> 0) & 0x0F;
        buffer[i*2+0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
        buffer[i*2+1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
    }
    buffer[len*2] = '\0';
}

void setup() {
  Serial.begin(9600);
  Serial.write("START");
  //while(Serial.available() == 0){}
  VCS.setup();
  
  Cart* cart = VCS.findCart();

  uint8_t romSegment[NBYTES];

  for (int offset = 0; offset < cart->size; offset += NBYTES) {
    VCS.dump(*cart, romSegment, offset, NBYTES);
    //char str[NBYTES] = "";
    //array_to_string(romSegment, NBYTES, str);
    //Serial.write(str);
    //Serial.write(' ');
    Serial.write(romSegment, NBYTES);
  }

  Serial.write("END");
}

void loop() {
  // nothing to see here folks...
}

//
//void setup() {
//  Serial.begin(9600);
//  VCS.setup();
//  
//  Cart* cart = VCS.findCart();
//
//  Serial.print("Cart Mapper Type: ");
//  Serial.println(VCS.getMapperName(cart->mapper));
//  
//  Serial.print("Cart ROM Size: ");
//  Serial.println(cart->size);
//  
//  Serial.print("Cart Bank Size: ");
//  Serial.println(cart->bankSize);
//  
//  Serial.print("Number of banks: ");
//  Serial.println(cart->bankCount);
//  
//  if (cart->ramSize > 0) {
//    Serial.print("Cart RAM Size: ");
//    Serial.println(cart->ramSize);
//  }
//}
