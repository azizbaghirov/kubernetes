import java.net.http.*;
import java.net.URI;
import java.nio.charset.StandardCharsets;

public class TerraformExecutor {
    public static void main(String[] args) {
        String terraformCommand = "terraform init && terraform apply -auto-approve";
        
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://terraform.tdac.svc.cluster.local:8080/run-terraform"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString("{\"command\":\"" + terraformCommand + "\"}"))
                .build();
            
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            
            System.out.println("Response: " + response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
