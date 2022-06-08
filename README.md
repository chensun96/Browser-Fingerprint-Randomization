# Privacy-Enhance-Spoofer
This is a repositary for a Law & Privay course project. This project is for the proof whether there is a relationship between browser fingerprint indentifers and stateless tracking.

We randomized values in browser fingerprint indentifers to verify our hypothesis.

experiment_Init.py is a python script to train personas (through browsing websites), and collect advertisements.

weblist.json contains websites will be visited to train personas. testlist.json contains websites will be used to collect advertisements.

Spoof folder includes files had been revised in google chrome to prevent stateless tracking. Geolocation, user agent, screen resolution, hardware concurrency, and device memory are browser fingerprint indentifers we focused.
