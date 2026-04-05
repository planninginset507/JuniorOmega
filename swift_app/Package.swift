// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "JuniorOmegaEdge",
    platforms: [
        .iOS(.v15), .macOS(.v13)
    ],
    products: [
        .library(name: "JuniorOmegaEdge", targets: ["JuniorOmegaEdge"]),
    ],
    dependencies: [
        .package(url: "https://github.com/grpc/grpc-swift.git", from: "1.21.0")
    ],
    targets: [
        .target(
            name: "JuniorOmegaEdge",
            dependencies: [
                .product(name: "GRPC", package: "grpc-swift"),
                .product(name: "NIO", package: "grpc-swift")
            ],
            path: "Sources"
        )
    ]
)
