import java.io.*;
import java.net.*;

public class TCPClient {
    public static void main(String[] args) {
        String host = "127.0.0.1";  // localhost IP
        int port = 65446;

        try (Socket socket = new Socket(host, port)) {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));

            String userInput;
            while (true) {
                System.out.print("Enter message for server (Q to quit): ");
                userInput = stdIn.readLine();
                if (userInput == null || userInput.equalsIgnoreCase("Q")) {
                    System.out.println("Client Disconnected...");
                    break;
                }

                out.write(userInput);
                out.newLine();
                out.flush();

                String response = in.readLine();
                if (response == null) {
                    System.out.println("Server disconnected.");
                    break;
                }
                System.out.println("Message from Server: " + response);
            }

        } catch (IOException e) {
            System.err.println("Client error: " + e.getMessage());
        }
    }
}
