#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <utility>
#include <cassert>
#include "ec_ops.h"
#include <ctime>
using namespace std;

Zp Zp::inverse() const{
	// Implement the Extended Euclidean Algorithm to return the inverse mod PRIME
	// Finds an x and y that satisfy the equation value(x) + PRIME(y) = 1 mod PRIME
	// We only care about x
	uberzahl P = PRIME;
	uberzahl V = value;

	uberzahl x("1");
	uberzahl y("0");
	
	while(V > 1)
	{
		uberzahl Q = V / P;

		uberzahl temp = P;
		P = V - P*(Q);
		V = temp;

		temp = y;
		y = x - (Q*y);
		x = temp;
	}

	return x;
}


ECpoint ECpoint::operator + (const ECpoint &a) const {
	// Implement  elliptic curve addition 		
	if (infinityPoint || a.infinityPoint)
		return this;

	//They are the same
	bool samePoint = (x == a.x) && (y == a.y);
	if (samePoint && !((y * Zp("2")) == Zp("0")))
	{
		Zp lambda = (((x*x) * Zp("3")) + A)*((y * Zp("2")).inverse());
		Zp xr = (lambda*lambda) - (x * Zp("2"));
		Zp yr = (y * Zp(-1)) + (lambda * (x - xr));
		return ECpoint(xr, yr);
	}
	if (!samePoint && !(x == a.x))
	{
		Zp lambda = (a.y - y)*((a.x - x).inverse());
		Zp xr = (lambda*lambda) - x - a.x;
		Zp yr = (y * Zp(-1)) + (lambda * (x - xr));
		return ECpoint(xr, yr);
	}


	return ECpoint(true);
}


ECpoint ECpoint::repeatSum(ECpoint p, uberzahl v) const {
	//Find the sum of p+p+...+p (vtimes)	
	//This is tail recursion so shouldn't run out of stack space.
	if (v == "0")
		return ECpoint(true);
	if (v == "1")
		return p;

	if ((v.bit(0)) == 0)
		return repeatSum(p + p, v / "2");
	else
		return p + repeatSum(p, v - "1");

	
}

Zp ECsystem::power(Zp val, uberzahl pow) {
	//Find the product of val*val*...*val (pow times)
	//This is tail recursion so shouldn't run out of stack space.
	if (pow == "0")
		return Zp("1");
	if (pow == "1")
		return val;

	if ((pow.bit(0)) == 0)
		return power(val * val, pow / "2");
	else
		return val * power(val * val, (pow - "1") / "2");
		
}



uberzahl ECsystem::pointCompress(ECpoint e) {
	//It is the gamma function explained in the assignment.
	//Note: Here return type is mpz_class because the function may
	//map to a value greater than the defined PRIME number (i.e, range of Zp)
	//This function is fully defined.	
	uberzahl compressedPoint = e.x.getValue();
	compressedPoint = compressedPoint<<1;
	
	if(e.infinityPoint) {
		cout<<"Point cannot be compressed as its INF-POINT"<<flush;
		abort();
		}
	else {
		if (e.y.getValue().bit(0) == 1)
			compressedPoint = compressedPoint + 1;
		}
		//cout<<"For point  "<<e<<"  Compressed point is <<"<<compressedPoint<<"\n";
		return compressedPoint;

}

ECpoint ECsystem::pointDecompress(uberzahl compressedPoint){
	//Implement the delta function for decompressing the compressed point
	Zp xr(compressedPoint / "2");
	smallType br = compressedPoint.bit(0);

	Zp z = (xr*xr*xr) + (xr * A) + B;

	uberzahl pow = (PRIME + "1") / "4";
	Zp yr1 = power(z, pow);
	Zp yr2 = Zp("-1") * power(z, pow);

	if ((yr1.getValue().bit(0)) == br)
		return ECpoint(xr, yr1);
	else
		return ECpoint(xr, yr2);
	
}


pair<pair<Zp,Zp>,uberzahl> ECsystem::encrypt(ECpoint publicKey, uberzahl privateKey,Zp plaintext0,Zp plaintext1){
	// You must implement elliptic curve encryption
	//  Do not generate a random key. Use the private key that is passed from the main function

	ECpoint Q = privateKey * G;
	ECpoint R = privateKey * publicKey;

	Zp C0 = plaintext0 * R.x;
	Zp C1 = plaintext1 * R.y;
	uberzahl C2 = pointCompress(Q);

	return make_pair(make_pair(C0,C1),C2);
}


pair<Zp,Zp> ECsystem::decrypt(pair<pair<Zp,Zp>, uberzahl> ciphertext){
	// Implement EC Decryption
	Zp C0 = ciphertext.first.first;
	Zp C1 = ciphertext.first.second;
	uberzahl C2 = ciphertext.second;

	ECpoint R = privateKey * pointDecompress(C2);

	Zp M0 = C0 * R.x.inverse();
	Zp M1 = C1 * R.y.inverse();

	return make_pair(M0,M1);
}


/*
 * main: Compute a pair of public key and private key
 *       Generate plaintext (m1, m2)
 *       Encrypt plaintext using elliptic curve encryption
 *       Decrypt ciphertext using elliptic curve decryption
 *       Should get the original plaintext
 *       Don't change anything in main.  We will use this to 
 *       evaluate the correctness of your program.
 */


int main(void){
	
	
	srand(time(0));
	ECsystem ec;
	unsigned long incrementVal;	
	pair <ECpoint, uberzahl> keys = ec.generateKeys();
	
	
	Zp plaintext0(MESSAGE0);
	Zp plaintext1(MESSAGE1);
	ECpoint publicKey = keys.first;
	cout<<"Public key is: "<<publicKey<<"\n";
	
	cout<<"Enter offset value for sender's private key"<<endl;
	cin>>incrementVal;
	uberzahl privateKey = XB + incrementVal;
	
	pair<pair<Zp,Zp>, uberzahl> ciphertext = ec.encrypt(publicKey, privateKey, plaintext0,plaintext1);	
	cout<<"Encrypted ciphertext is: ("<<ciphertext.first.first<<", "<<ciphertext.first.second<<", "<<ciphertext.second<<")\n";
	pair<Zp,Zp> plaintext_out = ec.decrypt(ciphertext);
	
	cout << "Original plaintext is: (" << plaintext0 << ", " << plaintext1 << ")\n";
	cout << "Decrypted plaintext: (" << plaintext_out.first << ", " << plaintext_out.second << ")\n";


	if(plaintext0 == plaintext_out.first && plaintext1 == plaintext_out.second)
		cout << "Correct!" << endl;
	else
		cout << "Plaintext different from original plaintext." << endl;
	

			
	return 0;

}


