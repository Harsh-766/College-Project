#include <iostream>
#include <unordered_map>
using namespace std;

// Node structure for Doubly Linked List
struct Node {
    string topic;
    int freq;
    Node* prev;
    Node* next;

    Node(string t) {
        topic = t;
        freq = 1;
        prev = next = NULL;
    }
};

class TrendingTracker {
    unordered_map<string, Node*> mp;
    Node* head;
    Node* tail;

public:
    TrendingTracker() {
        head = tail = NULL;
    }

    // Add new topic or update existing
    void addTopic(string topic) {
        if (mp.find(topic) == mp.end()) {
            Node* newNode = new Node(topic);

            if (!head) {
                head = tail = newNode;
            } else {
                tail->next = newNode;
                newNode->prev = tail;
                tail = newNode;
            }

            mp[topic] = newNode;
            cout << "Topic added!\n";
        } else {
            Node* node = mp[topic];
            node->freq++;
            reposition(node);
            cout << "Topic updated!\n";
        }
    }

    // Move node forward based on frequency
    void reposition(Node* node) {
        while (node->prev && node->freq > node->prev->freq) {
            Node* prevNode = node->prev;
            Node* nextNode = node->next;

            // Swap node with prevNode
            if (prevNode->prev)
                prevNode->prev->next = node;
            node->prev = prevNode->prev;

            node->next = prevNode;
            prevNode->prev = node;

            prevNode->next = nextNode;
            if (nextNode)
                nextNode->prev = prevNode;

            // Update head/tail
            if (prevNode == head)
                head = node;
            if (node == tail)
                tail = prevNode;
        }
    }

    // Display all topics
    void display() {
        if (!head) {
            cout << "No topics available!\n";
            return;
        }

        cout << "\nTrending Topics:\n";
        Node* temp = head;
        int rank = 1;

        while (temp) {
            cout << rank++ << ". " << temp->topic << " ("
                 << temp->freq << ")\n";
            temp = temp->next;
        }
    }

    // Show Top K topics
    void topK(int k) {
        Node* temp = head;
        int count = 0;

        cout << "\nTop " << k << " Topics:\n";

        while (temp && count < k) {
            cout << temp->topic << " (" << temp->freq << ")\n";
            temp = temp->next;
            count++;
        }
    }

    // Search topic
    void search(string topic) {
        if (mp.find(topic) != mp.end()) {
            Node* node = mp[topic];
            cout << topic << " found with frequency "
                 << node->freq << endl;
        } else {
            cout << "Topic not found!\n";
        }
    }

    // Delete topic
    void deleteTopic(string topic) {
        if (mp.find(topic) == mp.end()) {
            cout << "Topic not found!\n";
            return;
        }

        Node* node = mp[topic];

        if (node->prev)
            node->prev->next = node->next;
        else
            head = node->next;

        if (node->next)
            node->next->prev = node->prev;
        else
            tail = node->prev;

        mp.erase(topic);
        delete node;

        cout << "Topic deleted!\n";
    }
};

int main() {
    TrendingTracker tracker;
    int choice;
    string topic;
    int k;

    do {
        cout << "\n===== Trending Topics Tracker =====\n";
        cout << "1. Add Topic Mention\n";
        cout << "2. Display All Topics\n";
        cout << "3. Show Top K Topics\n";
        cout << "4. Search Topic\n";
        cout << "5. Delete Topic\n";
        cout << "0. Exit\n";
        cout << "Enter choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter topic: ";
                cin >> topic;
                tracker.addTopic(topic);
                break;

            case 2:
                tracker.display();
                break;

            case 3:
                cout << "Enter K: ";
                cin >> k;
                tracker.topK(k);
                break;

            case 4:
                cout << "Enter topic: ";
                cin >> topic;
                tracker.search(topic);
                break;

            case 5:
                cout << "Enter topic: ";
                cin >> topic;
                tracker.deleteTopic(topic);
                break;
        }

    } while (choice != 0);

    return 0;
}