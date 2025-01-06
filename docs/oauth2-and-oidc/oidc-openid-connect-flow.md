---
icon: lock-keyhole
---

# OIDC: OpenID Connect Flow

> **`OIDC`:** **OpenID Connect**:
>
> an identity layer built on top of the OAuth 2.0 protocol

* allows clients to verify the identity of the end-user&#x20;
  * based on the authentication performed by an `authorization server`

## Key Components:

1. `User`**: Resource Owner**: The end-user who owns the data.
2. `Relying Party`**: Client**: The application requesting access on behalf of the user&#x20;
   * client application — service provider
3. `Identity Provider`**: Authorization Server**: The server that issues tokens after authenticating the user.
4. `Resource Server`: The server that hosts the protected resources and accepts tokens for access.



```http
{
    "sub": "1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

## Step-by-Step OIDC Authentication Flow:

1.  **Authorization Request**:

    * The client redirects the user to the authorization server’s authorization endpoint.
    * The request includes parameters like `client_id`, `redirect_uri`, `response_type`, `scope`, and `state`.

    ```http
    GET /authorize?
        response_type=code&
        client_id=CLIENT_ID&
        redirect_uri=REDIRECT_URI&
        scope=openid profile email&
        state=STATE
    ```




2.  **User Authentication**:

    * The authorization server authenticates the user (e.g., via login form).
    * If the user is already authenticated, this step might be skipped.


3.  **Authorization Grant**:

    * After successful authentication, the authorization server asks the user to grant access to the client.
    * If the user approves, the server redirects the user to the client’s `redirect_uri` with an authorization code.

    ```http
    GET /callback?code=AUTH_CODE&state=STATE
    ```




4.  **Token Request**:

    * The client exchanges the authorization code for tokens by making a POST request to the authorization server’s token endpoint.
    * The request includes parameters like `grant_type`, `code`, `redirect_uri`, `client_id`, and `client_secret`.

    ```http
    POST /token
    Content-Type: application/x-www-form-urlencoded

    grant_type=authorization_code&
    code=AUTH_CODE&
    redirect_uri=REDIRECT_URI&
    client_id=CLIENT_ID&
    client_secret=CLIENT_SECRET
    ```




5.  **Token Response**:

    * The authorization server responds with an ID token and access token.

    ```json
    {
        "access_token": "ACCESS_TOKEN",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "ID_TOKEN"
    }
    ```




6.  **User Information Request**:

    * The client can request additional user information from the UserInfo endpoint using the access token.

    ```http
    GET /userinfo
    Authorization: Bearer ACCESS_TOKEN
    ```




7.  **User Information Response**:

    * The authorization server responds with the user’s profile information.

    ```json
    {
        "sub": "1234567890",
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    ```

\
