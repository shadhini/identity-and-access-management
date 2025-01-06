---
icon: cabinet-filing
---

# Keystores & Truststores

**`Keystore`** — a repository that holds the keys and certificates of a trust chain

* In a Keystore, you can store both private and public keys.&#x20;

**`Truststore`** — a repository that is protected by a password, which stores digital certificates





## Keytool Commands  <a href="#id-1d56" id="id-1d56"></a>

* Create a keystore&#x20;

`keytool -genkey -alias wso2carbon -keyalg RSA 2048 -keystore wso2carbon.jks -dname "CN=localhost, OU=Home, L=SL, S=WS, C=LK" -storepass wso2carbon -keypass wso2carbon -validity 360 -ext "SAN=DNS:localhost.com"`

* List keystore&#x20;

`keytool -list -keystore wso2carbon.jks -storepass wso2carbon`

* Extend keystore&#x20;

`keytool -list -v -keystore wso2carbon.jks -storepass wso2carbon`

* Take the keystore list to a file&#x20;

`keytool -list -v -keystore wso2carbon.jks -storepass wso2carbon >> keystore.txt`

* Export certificate&#x20;

`keytool -exportcert -keystore wso2carbon.jks -alias wso2carbon -file wso2carbon.crt`

* Import certificate&#x20;

`keytool -importcert -keystore client-truststore.jks -alias wso2carbon2 -file wso2carbon.crt`

* Creating a CSR using JKS&#x20;

`keytool -certreq alias -wso2carbon_1 -file wso2carbon.csr -keystore newkeystore -storepass mypassword`

* Creating a PEM file using JKS&#x20;

`keytool -certreq -v -alias wso2carbon_1 -file csr-for-wso2carbon.pem -keypass mypassword -storepass mypassword -keystore newkeystore.jks`

* Add CA root and intermediate certificates to JKS&#x20;

`keytool -import -v -trustcacerts -alias ca_bundle -file ca_bundle.crt -keystore newkeystore.jks -storepass mypassword`

* Adding the CA signed SSL/TLS certificate to keystore&#x20;

`keytool -import -v -alias wso2carbon_1 -file certificate.crt -keystore newkeystore -keypass mypassword -storepass mypassword`



