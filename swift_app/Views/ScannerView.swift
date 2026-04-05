// swift_app/Views/ScannerView.swift
import SwiftUI

struct ScannerView: View {
    @StateObject private var engine = TrueDepthEngine()
    
    var body: some View {
        ZStack {
            Color(red: 0.04, green: 0.04, blue: 0.04).edgesIgnoringSafeArea(.all)
            
            VStack {
                Text("JUNIORCLOUD OMEGA EDGE")
                    .font(.custom("CourierNewPS-BoldMT", size: 20))
                    .foregroundColor(Color(red: 0.83, green: 0.68, blue: 0.21))
                    .padding()
                
                Spacer()
                
                VStack(alignment: .leading, spacing: 10) {
                    Text("TRUEDEPTH MESH: \(engine.activeVertices) VERTICES")
                        .foregroundColor(.green)
                    Text("SVD ENGINE: AWAITING PAYLOAD")
                        .foregroundColor(.white)
                }
                .font(.system(size: 16, weight: .bold, design: .monospaced))
                
                Spacer()
                
                Button(action: { engine.startSession() }) {
                    Text("ENGAGE SPATIAL CAPTURE")
                        .font(.headline)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color(red: 0.83, green: 0.68, blue: 0.21))
                        .foregroundColor(.black)
                        .cornerRadius(8)
                }
                .padding()
            }
        }
    }
}
