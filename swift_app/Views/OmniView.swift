import SwiftUI

struct OmniView: View {
    @StateObject private var engine = OmniScannerEngine()
    
    var body: some View {
        ZStack {
            Color(red: 0.04, green: 0.04, blue: 0.04).edgesIgnoringSafeArea(.all)
            VStack {
                Text("JUNIOROMEGA EDGE INGEST")
                    .font(.system(size: 20, weight: .bold, design: .monospaced))
                    .foregroundColor(Color(red: 0.83, green: 0.68, blue: 0.21))
                    .padding()
                
                Spacer()
                
                VStack(alignment: .leading, spacing: 12) {
                    Text("SPATIAL MANIFOLD: \(engine.vertexCount) PTS")
                        .foregroundColor(engine.vertexCount > 0 ? .green : .red)
                    Text("GRPC TARGET: localhost:50051")
                        .foregroundColor(.gray)
                }
                .font(.system(size: 14, weight: .medium, design: .monospaced))
                
                Spacer()
                
                Button(action: { engine.engageScanner() }) {
                    Text("INITIALIZE CAPTURE")
                        .font(.headline)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color(red: 0.83, green: 0.68, blue: 0.21))
                        .foregroundColor(.black)
                        .cornerRadius(4)
                }
                .padding()
            }
        }
    }
}
