---
description: Keystore and Truststore in WSO2 Identity Server
icon: cabinet-filing
---

# Keystores & Truststores

## Keystores & Truststores

WSO2 IS default keystore file and truststore file are located in `<IS_HOME>/repository/resources/security` directory.

* `wso2carbon.jks` — default Keystore&#x20;
  * contains&#x20;
    * a private key &#x20;
    * the self-signed public-key certificate
* `client-truststore.jks` — default truststore&#x20;
  * contains certificates of reputed CAs that can validate the identity of third-party systems
  * also contains the self-signed certificate of the default `wso2carbon.jks` keystore
  * default password: `wso2carbon`



In general WSO2 IS have 4 types of keystores.

* Primary Keystore — Encrypt the data going outside the IS (e.g. JWT token).
* Internal Keystore — Encrypt the critical data inside the IS.
* SSL/TLS Keystore — To facilitate SSL/TLS connection.
* Truststore — To contain the digital certificates.

If you open `<IS_HOME>/repository/conf/deployment.toml` file you can see that the primary keystore has been set to `wso2carbon.jks`

```
[keystore.primary]
file_name = wso2carbon.jks
password = wso2carbon[truststore]
file_name="client-truststore.jks"
password="wso2carbon"
type="JKS"
```

*   If you do not specify separate keystores for internal and SSL/TLS purposes, the provided code snippet ensures that both keystores use the same `wso2carbon.jks` file, which is the same as the primary [keystore](https://www.java67.com/2012/09/keytool-command-examples-java-add-view-certificate-ssl.html).





## Keystores configuration beyond `deployment.toml` file

* Primary and Internal Keystores → `<IS_HOME>/repository/conf/carbon.xml`
* SSL/TLS Keystore → `<IS_HOME>/repository/conf/tomcat/catalina-server.xml`
* Truststore → `<IS_HOME>/repostitory/conf/carbon.xml`

&#x20;

## How we can add a new SSL/TLS certificate to a keystore and configure it in the WSO2 IS

### Creating a Certificate using a Keystore <a href="#id-3c17" id="id-3c17"></a>

1. Creating a self-signed certificate
2. Creating a CA-signed certificate



### _Creating a self-signed certificate and adding it to the Truststore_ <a href="#id-26b8" id="id-26b8"></a>

#### Generate a **new keystore** that includes a private key&#x20;

Navigate to `<IS_HOME>/repository/resources/security` and execute the command

```bash
keytool -genkey -alias <PUBLIC_CERT_ALIAS> -keyalg RSA -keysize 2048 -keystore <KEY_STORE_NAME>.jks -dname "CN=<COMMON_NAME>, OU=<ORGANIZATIONAL_UNIT>, O=<ORGANIZATION>, L=<LOCALITY>, S=<STATE>, C=<COUNTRY>" -storepass <KEYSTORE_PASSWORD> -keypass <PRIVATE_KEY_PASSWORD>
```

* Common Name should be the domain name.

```bash
keytool -genkey -alias wso2carbon_1 -keyalg RSA -keysize 2048 -keystore newkeystore.jks -dname "CN=localhost, OU=Home, O=Home, L=SL, S=WS, C=LK" -storepass mypassword -keypass mypassword
```



#### Export the public certificate using the created JKS file

```
keytool -exportcert -keystore newkeystore.jks -alias wso2carbon_1 -file wso2carbon.crt
```

* You will get a certificate named `wso2carbon.crt`&#x20;
* Since this is a self-signed certificate we need to add this to `client-truststore.jks`&#x20;



#### Add self-signed public certificate to truststore

```
keytool -importcert -keystore client-truststore.jks -alias wso2carbon_1 -file wso2carbon.crt
```



#### View the keys of the Truststore&#x20;

```
keytool -list -v -keystore client-truststore.jks -storepass wso2carbon
```





#### Remove certificate from the Truststore

Since there's already a certificate linked to `localhost` by default with `wso2carbon` alias, remove it in the truststore.

```
keytool -delete -noprompt -alias wso2carbon -keystore client-truststore.jks -storepass wso2carbon
```



#### Set newly created keystore as TLS keystore in the `deployment.toml`&#x20;

`<IS_HOME>/repository/conf/deployment.toml`&#x20;

```
[keystore.tls]
file_name = "newkeystore.jks"
type = "JKS"
password = "mypassword"
alias = "wso2carbon_1"
key_password = "mypassword"
```



#### Start WSO2 IS server

when you start the WOS2 IS and go to `localhost:9443`, you'll see that the `Certificate is not valid` & `Not Secure`

And then you can find our self-signed certificate is added correctly.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*xukDkOoFPFoe8lfDP6EuLw.png" alt="" height="278" width="700"><figcaption><p>Not secure in the browser address bar</p></figcaption></figure>

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*rjJGORxAlfw9t2qqQ1PRoA.png" alt="" height="419" width="700"><figcaption><p>Self-signed certificate</p></figcaption></figure>



### \*\* Creating a CA-signed certificate and adding it to the Truststore <a href="#id-0add" id="id-0add"></a>

Get a fresh WSO2 IS pack and create a new JSK file inside the `<IS_HOME>/repository/resources/security` directory.

```
keytool -genkey -alias wso2carbon_1 -keyalg RSA -keysize 2048 -keystore newkeystore.jks -dname "CN=nipunaupekshatest95.tk, OU=Home, O=Home, L=SL, S=WS, C=LK" -storepass mypassword -keypass mypassword
```

Here, the common name (CN) used is `nipunaupekshatest95.tk`, which should be the domain name.&#x20;

{% hint style="info" %}
While you can use `localhost` for CN, it cannot receive digitally certified certificates from a verified CA.&#x20;

However, you can obtain a free `.tk` domain from [Freenom](https://www.freenom.com/en/index.html?lang=en) and use it.
{% endhint %}



#### View what is in your keystore&#x20;

```
keytool -list -v -keystore mykeystore.jks -storepass mypassword
```

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*W3qRMh58vqPEfXC2JOyqdA.png" alt="" height="438" width="700"><figcaption><p>Check our keystore</p></figcaption></figure>

{% hint style="warning" %}
**To make certificate valid**,  Make a certificate signing request file(`CSR`) and then certify it by a certification authority(`CA`).&#x20;
{% endhint %}



#### Make a CSR: Certificate Signing Request

Approach 1: directly creating a CSR and submitting it to a CA.&#x20;

```
keytool -certreq -alias wos2carbon_1 -file wso2carbon.csr -keystore newkeystore.jks -storepass mypassword
```



Approach 2: creating a `.pem` file (`Privacy Enhanced Mail` file) and submit it to a CA.&#x20;

```
keytool -certreq -v -alias wso2carbon_1 -file csr-for-wso2carbon.pem -keypass mypassword -storepass mypassword -keystore newkeystore.jks
```



#### Certify CSR/PEM from a CA

You can sign one for free from [SSLForFree](https://www.sslforfree.com/).&#x20;

1. Create an account &#x20;
2. Go to get a new certificate
3. Type cert CN name (e.g. `nipunaupekshatest95.tk`) as your domain.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*SSjoOtYXpakZiu14lB5ITw.png" alt="" height="384" width="700"><figcaption><p>Adding domain for certificate</p></figcaption></figure>

4. `validity period` —  a 90-day certificate
5. `CSR & Contract` — select paste existing CSR
   * open, the `csr-for-wso2carbon.pem` or `wso2carbon.csr` from [VSCode ](https://medium.com/javarevisited/8-best-vs-code-courses-for-beginners-to-learn-online-bd5c169f59b7)or Notepad and copy and paste the content there.
6. Finalize your order.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*28ZjEuCbt9SVkR9w6ZrzbA.png" alt="" height="384" width="700"><figcaption><p>Finalizing the order</p></figcaption></figure>

7. verify your domain
   * verify it using DNS(CNAME)

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*gdnj9k-CaDbKXKMwF5r2Lg.png" alt="" height="384" width="700"><figcaption><p>DNS(CNAME) selected</p></figcaption></figure>

8. Go to your freenom account and select the domain you got and select “Manage Freenom DNS”

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*SZfrqQ2y53XrxzTIc-dmwA.png" alt="" height="384" width="700"><figcaption><p>Freenom domain</p></figcaption></figure>

9. Copy and paste the values accordingly.
10. type — select CNAME

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*yWjicAxkrat70K0M84LYIw.png" alt="" height="384" width="700"><figcaption><p>Add DNS</p></figcaption></figure>

11. click `Save Changes`in freenom and go to `SSLForFree` website and go to next step and click on `Verify Domain`.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*ahokXCQCvtZKNpdF5IhNBw.png" alt="" height="384" width="700"><figcaption><p>SSLForFree domain verification</p></figcaption></figure>

* If everything went well and waited enough time, the server will realize that the domain actually belongs to you and issue you a CA-signed certificate.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*7J0j3uGDm5OSqRsVdTKvoQ.png" alt="" height="384" width="700"><figcaption><p>Domain verified</p></figcaption></figure>

* After that, you will receive a mail saying that the domain is certified. You can download the certificate by going to the certifications section in the SSLForFree.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*beSkRMswVedKBXA488u2OA.png" alt="" height="384" width="700"><figcaption><p>Download CA certified certificate</p></figcaption></figure>

`ca_bundle.crt` —  the CA root certificate and a set of intermediate certificates `certificate.crt` —  the CA-signed certificate



#### Add CA root certificate and intermediate certificates  to keystore

```
keytool -import -v -trustcacerts -alias ca_bundle -file ca_bundle.crt -keystore newkeystore.jks -storepass mypassword
```





#### Add CA-signed SSL certificate to the keystore&#x20;

* Make sure that you use the same alias that you used while creating the keystore.

```
keytool -import -v -alias wso2carbon_1 -file certificate.crt -keystore newkeystore -keypass mypassword -storepass mypassword
```



#### Add certs to Truststore

Add to truststore to trust it as an SSL/TLS certificate.&#x20;

1. Extract the public key from keystore

```
keytool -export -alias wso2carbon_1 -keystore newkeystore.jks -file wso2carbon_1_public_key.pem
```



2. Add public key to the `client-truststore.jks`

```
keytool -import -alias wso2carbon_1 -file wso2carbon_1_public_key.pem -keystore client-truststore.jks -storepass wso2carbon
```



#### Configure IS deployment.toml

1. Rename the `wso2carbon.jks` file to `internal.jks` and `newkeystore.jks` file to `wso2carbon.jks`&#x20;
2. Update  config  in `<IS_HOME>/repository/conf/deployment.toml` file director

&#x20;an alternative way of configuring`keystore.tls` setting in the `deployment.toml` file.

```
[server]
hostname = "nipunaupekshatest95.tk"
node_ip = "127.0.0.1"
base_path = "https://$ref{server.hostname}:${carbon.management.port}"[keystore.primary]
file_name = "wso2carbon.jks"
password = "mypassword"
alias = "wso2carbon_1"[keystore.internal]
file_name = "internal.jks"
password = "wso2carbon"
alias = "wso2carbon"
```



#### Start IS server

Now, if you go to `nipunaupekshatest95.tk:9443/carbon` you will be able to see that the website is secured.



