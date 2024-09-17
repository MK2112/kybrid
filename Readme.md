# kybrid

As simple as it gets full-stack web application with hybrid encryption using RSA for front-to-back communication and post-quantum encryption (Kyber) in the backend, which is displayed then to the user.

- Frontend encrypts user input using RSA, 
- Frontend sends encrypted input to backend, 
- Backend decrypts it 
- Backend applies post-quantum encryption
- Backend returns the pq-encrypted result
- Frontend displays the result.

I'm aware that using RSA for the initial communication is not the most secure approach, especially in a post-quantum world some undeterminable time in the future. Ideally, the entire process should be post-quantum encrypted and layered with additional encryption and more measures for proof of authenticity, etc.<br>
However, this project is designed to demonstrate a hybrid encryption-decryption approach only. I will be further experimenting here with post-quantum encryption and other cryptographic methods in the future. (Assume this project's annealing temperature to be high)

## Setup

```bash
pip install -r requirements.txt
```

```bash
python backend.py
python frontend.py
```

Open your browser at `http://127.0.0.1:5001/`.