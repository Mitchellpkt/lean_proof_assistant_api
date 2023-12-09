## Lean proof assistant

Mitchell Krawiec-Thayer - 2023

## Description

A simple flask app that wraps the standard lean proof assistant library and exposes it as a REST API. The interface is JSON-in/JSON-out, intended to be compatible with the OpenAI "function calling" described here: https://platform.openai.com/docs/guides/function-calling

This is a research prototype that is not in any way robust or secure.

## Server setup (Linux)

These are **very hacky non-production grade** instructions for how to host a server. If you just want to send queries to an existing endpoint, skip to the next big section (Example API calls & responses).


### Install Dependencies
To install directly to base, you can simply run:

```bash
./install_dependencies.sh
```

(You may need to `chmod +x install_dependencies.sh` first, so the script permissions include execution.)

### Launch server
```bash
python3 app.py
```

## Example API calls & responses

These are instructions for how to use the API. 

Replace `<HOST>` and `<PORT>` with the information for your server.

### Valid proof

Successful proofs return `"status":"success"`.

#### Submission

```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"proof":"example : 1 + 1 = 2 := rfl"}' \
    http://<HOST>:<PORT>/verify-lean-proof
```

#### Response

```
{"message":"Proof is valid","output":"","status":"success"}
```

### Failed proof

Failed proofs return `"status":"error"`. Information about the reason why may be included in the `"output"` and/or `"error"` fields.

#### Submission

```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"proof":"import fake_library.nonexistent\n\nexample : 1 + 1 = 2 := rfl"}' \
    http://<HOST>:<PORT>/verify-lean-proof
```

#### Response

```
{
    "status":"error"
    "message":"Proof is invalid",
    "output":"temp_proof.lean:1:0: error: unknown package 'fake_library'\ntemp_proof.lean:3:11: error: unexpected token '+'; expected ':=', 'where' or '|'\n",
    "error":"",
}
```