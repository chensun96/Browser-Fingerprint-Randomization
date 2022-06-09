# Privacy-Enhance-Spoofer
This is a repositary for a Law & Privay course project. This project is for the proof whether there is a relationship between browser fingerprint indentifers and stateless tracking.

We randomized values in browser fingerprint indentifers to verify our hypothesis.

experiment_Init.py is a python script to train personas (through browsing websites), and collect advertisements.

weblist.json contains websites were visited to train personas. testlist.json contains websites were used to collect advertisements.

Spoof folder includes files had been revised in google chrome to prevent stateless tracking. Geolocation, user agent, screen resolution, hardware concurrency, and device memory were browser fingerprint indentifers we focused on.

googleVision.py in analyze folder is a python script to use Google vision APU to categorize advertisements we collected.
