import java.io.*;
import java.net.*;

public class TCPServer {
    public static void main(String[] args) {
        String host = "127.0.0.1";  // localhost IP
        int port = 65446;

        try (ServerSocket serverSocket = new ServerSocket()) {
            serverSocket.bind(new InetSocketAddress(host, port));
            System.out.println("TCP Server connecting on " + host + ":" + port + "...");

            Socket clientSocket = serverSocket.accept();
            System.out.println("Connected by " + clientSocket.getRemoteSocketAddress());

            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));

            String clientMsg;
            while ((clientMsg = in.readLine()) != null) {
                System.out.println("Client says: " + clientMsg);

                System.out.print("Enter reply to Client: ");
                String reply = stdIn.readLine();
                if (reply == null) break;

                out.write(reply);
                out.newLine();
                out.flush();
            }

            System.out.println("Client disconnected.");
            clientSocket.close();

        } catch (IOException e) {
            System.err.println("Server error: " + e.getMessage());
        }
    }
}
