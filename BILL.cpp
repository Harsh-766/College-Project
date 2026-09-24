#include <iostream>
#include <ctime>
#include <string>
#include <vector>
using namespace std;
 
struct Product {
    int code;
    string name;
    double price;
    double discount; // 0.1 for 10%, 0 for no discount
};

class ItemPurchaseSystem {
private:
    vector<Product> products;
    double totalAmount;

    void showAuthorDetails() {
        cout <<"-------------------------------------------------------------------\n";
        cout <<"             ***  Project : General Store Management System  ***\n";
        cout <<"-------------------------------------------------------------------\n";
        cout <<"                 Author  - [ github - lokesh209601 , Harshvardhanchaudhary7 ]\n";  
        cout <<"                 Created - 25/10/2025\n";
        cout <<"                 Program - Dev-C++\n";
        cout <<"*******************************************************************\n";
    }

    void printLine() { cout << endl; }

    void printDoubleLine() { cout << endl << endl; }

    void showTitleAndTime() {
        time_t t = time(0);
        struct tm* tt = localtime(&t);
        system("cls");
        showAuthorDetails();
        printDoubleLine();
        cout << "**** The Bros beverage corporation (Pvt) Ltd **** Mohali branch India ****" << endl;
        cout << "**** Current date & time : " << asctime(tt);
    }

    void showMenu() {
        cout << "\n------------------------- * MENU LIST * --------------------------" << endl;
        cout << "Code | Juice type | Price Rs. | Buy 5 get 10% off" << endl;
        for (auto &p : products) {
            cout << p.code << "       " << p.name << "         " << p.price << "        "
                 << (p.discount > 0 ? "Yes" : "No") << endl;
        }
    }

    void calculateBill() {
        totalAmount = 0;
        char continueShopping = 'y';
        vector<int> quantities(products.size(), 0);
        vector<double> itemTotals(products.size(), 0);

        while (continueShopping == 'y' || continueShopping == 'Y') {
            showMenu();
            int code, qty;
            cout << "\nEnter Item code (0 to finish): ";
            cin >> code;
            if (code == 0) break;

            cout << "Quantity: ";
            cin >> qty;

            bool found = false;
            for (size_t i = 0; i < products.size(); i++) {
                if (products[i].code == code) {
                    found = true;
                    quantities[i] += qty;
                    double amount = qty * products[i].price;
                    if (qty >= 5 && products[i].discount > 0) {
                        amount *= (1 - products[i].discount);
                    }
                    itemTotals[i] += amount;
                    totalAmount += amount;
                    cout << "Added " << qty << " x " << products[i].name << " to bill. Amount: " << amount << endl;
                    break;
                }
            }
            if (!found) {
                cout << "Invalid item code! Try again.\n";
            }

            cout << "Do you want to add more items? (y/n): ";
            cin >> continueShopping;
        }

        // Display final bill
        system("cls");
        showTitleAndTime();
        cout << "\n**** Purchased items ****" << endl;
        cout << "Juice Type\tPrice\tQty\tAmount\tDiscount\n";
        for (size_t i = 0; i < products.size(); i++) {
            if (quantities[i] > 0) {
                double discountApplied = (quantities[i] >= 5 && products[i].discount > 0) ? products[i].discount * products[i].price * quantities[i] : 0;
                cout << products[i].name << "\t" "\t"<< products[i].price << "\t"  << quantities[i] 
                     << "\t" << itemTotals[i] << "\t" << discountApplied << endl;
            }
        }
        cout << "Total Amount: Rs." << totalAmount << "/=" << endl;

        // Payment handling
        double paid = 0;
        while (paid < totalAmount) {
            double cash;
            cout << "Pay Amount in Cash: ";
            cin >> cash;
            paid += cash;
            if (paid < totalAmount) {
                cout << "Payment insufficient. Remaining: " << totalAmount - paid << endl;
            }
        }
        cout << "Payment completed! Balance: " << paid - totalAmount << "/=\n";
        cout << "Thank you for your purchase!\n";
    }

public:
    ItemPurchaseSystem() {
        // Initialize products
        products = {
            {1, "Apple", 120, 0},
            {2, "Orange", 100, 0.1},
            {3, "Mango", 90, 0.1},
            {4, "Graps", 130, 0},
            {5, "Avacado", 140, 0.1}
        };
    }

    void start() {
        showTitleAndTime();
        char option;
        do {
            cout << "\nSelect Option:\n(M) MENU DETAILS\n(B) BILL\n(E) EXIT\nOption: ";
            cin >> option;
            switch (option) {
                case 'M':
                    system("cls");
                    showTitleAndTime();
                    showMenu();
                    break;
                case 'B':
                    calculateBill();
                    break;
                case 'E':
                    cout << "Exiting...\n";
                    return;
                default:
                    cout << "Invalid option! Try again.\n";
            }
        } while (true);
    }
};

int main() {
    ItemPurchaseSystem system;
    system.start();
    return 0;
}
