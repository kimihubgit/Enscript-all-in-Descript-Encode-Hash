import cn.hutool.core.codec.Base64;

import javax.crypto.Cipher;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.spec.X509EncodedKeySpec;

public class Test {
    public static void main(String[] args) throws Exception {
        //用户密码
        String password = "abcdef";
        //获取到的证书内容
        String key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDjb4V7EidX/ym28t2ybo0U6t0n\n6p4ej8VjqKHg100va6jkNbNTrLQqMCQCAYtXMXXp2Fwkk6WR+12N9zknLjf+C9sx\n/+l48mjUU8RqahiFD1XT/u2e0m2EN029OhCgkHx3Fc/KlFSIbak93EH/XlYis0w+\nXl69GV6klzgxW6d2xQIDAQAB\n-----END PUBLIC KEY-----\n";
        //获取到的盐值
        String hash = "bb73382121594c46";
        String[] split = key.strip().split("\n");
        String newKey = split[1] + split[2] + split[3] + split[4];
        //进行加密
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(Base64.decode(newKey));
        PublicKey publicKey = keyFactory.generatePublic(keySpec);
        Cipher cipher = Cipher.getInstance(keyFactory.getAlgorithm());
        cipher.init(Cipher.PUBLIC_KEY, publicKey);
        byte[] bytes = cipher.doFinal((hash + password).getBytes());
        String encode = Base64.encode(bytes);
        System.out.println(encode);
    }
}