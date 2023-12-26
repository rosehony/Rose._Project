import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;

public class FileEncryptionService {

    private static final String ALGORITHM = "AES";
    private static final String TRANSFORMATION = "AES";

    public static void encryptFile(InputStream inputStream, OutputStream outputStream, String key)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, IOException,
            BadPaddingException, IllegalBlockSizeException {

        Key secretKey = new SecretKeySpec(key.getBytes(), ALGORITHM);
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);

        byte[] inputBytes = inputStream.readAllBytes();
        byte[] outputBytes = cipher.doFinal(inputBytes);

        outputStream.write(outputBytes);
    }

    public static void decryptFile(InputStream inputStream, OutputStream outputStream, String key)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, IOException,
            BadPaddingException, IllegalBlockSizeException 
            {

        Key secretKey = new SecretKeySpec(key.getBytes(), ALGORITHM);
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);

        byte[] inputBytes = inputStream.readAllBytes();
        byte[] outputBytes = cipher.doFinal(inputBytes);

        outputStream.write(outputBytes);
    }
}



