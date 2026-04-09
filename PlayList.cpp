#include <iostream>
using namespace std;

// Node structure
struct Song {
    string name;
    Song* prev;
    Song* next;
};

// Playlist class
class Playlist {
private:
    Song* head;
    Song* tail;
    Song* current;

public:
    Playlist() {
        head = tail = current = NULL;
    }

    // Add song
    void addSong(string name) {
        Song* newSong = new Song{ name, NULL, NULL };

        if (head == NULL) {
            head = tail = newSong;
        } else {
            tail->next = newSong;
            newSong->prev = tail;
            tail = newSong;
        }

        cout << "Song added: " << name << endl;
    }

    // Remove song
    void removeSong(string name) {
        Song* temp = head;

        while (temp != NULL) {
            if (temp->name == name) {
                if (temp == head) head = temp->next;
                if (temp == tail) tail = temp->prev;
                if (temp->prev) temp->prev->next = temp->next;
                if (temp->next) temp->next->prev = temp->prev;

                delete temp;
                cout << "Song removed: " << name << endl;
                return;
            }
            temp = temp->next;
        }

        cout << "Song not found!" << endl;
    }

    // Play first
    void playFirst() {
        if (head == NULL) {
            cout << "Playlist is empty!" << endl;
            return;
        }
        current = head;
        cout << "Playing: " << current->name << endl;
    }

    // Play last
    void playLast() {
        if (tail == NULL) {
            cout << "Playlist is empty!" << endl;
            return;
        }
        current = tail;
        cout << "Playing: " << current->name << endl;
    }

    // Play next
    void playNext() {
        if (current == NULL || current->next == NULL) {
            cout << "No next song!" << endl;
            return;
        }
        current = current->next;
        cout << "Playing: " << current->name << endl;
    }

    // Play previous
    void playPrevious() {
        if (current == NULL || current->prev == NULL) {
            cout << "No previous song!" << endl;
            return;
        }
        current = current->prev;
        cout << "Playing: " << current->name << endl;
    }

    // Play specific song
    void playSpecific(string name) {
        Song* temp = head;

        while (temp != NULL) {
            if (temp->name == name) {
                current = temp;
                cout << "Playing: " << current->name << endl;
                return;
            }
            temp = temp->next;
        }

        cout << "Song not found!" << endl;
    }

    // Display playlist
    void display() {
        Song* temp = head;
        cout << "\nPlaylist:\n";
        while (temp != NULL) {
            cout << temp->name << " -> ";
            temp = temp->next;
        }
        cout << "NULL\n";
    }
};

// Main function
int main() {
    Playlist p;
    int choice;
    string song;

    do {
        cout << "\n--- MUSIC PLAYLIST MENU ---\n";
        cout << "1. Add Song\n";
        cout << "2. Remove Song\n";
        cout << "3. Play First\n";
        cout << "4. Play Last\n";
        cout << "5. Play Next\n";
        cout << "6. Play Previous\n";
        cout << "7. Play Specific Song\n";
        cout << "8. Display Playlist\n";
        cout << "0. Exit\n";
        cout << "Enter choice: ";
        cin >> choice;

        switch (choice) {
        case 1:
            cout << "Enter song name: ";
            cin >> song;
            p.addSong(song);
            break;

        case 2:
            cout << "Enter song name to remove: ";
            cin >> song;
            p.removeSong(song);
            break;

        case 3:
            p.playFirst();
            break;

        case 4:
            p.playLast();
            break;

        case 5:
            p.playNext();
            break;

        case 6:
            p.playPrevious();
            break;

        case 7:
            cout << "Enter song name: ";
            cin >> song;
            p.playSpecific(song);
            break;

        case 8:
            p.display();
            break;

        case 0:
            cout << "Exiting...\n";
            break;

        default:
            cout << "Invalid choice!\n";
        }

    } while (choice != 0);

    return 0;
}