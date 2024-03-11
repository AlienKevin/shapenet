import SceneKit
import Cocoa

class ViewController: NSViewController {
    var sceneView: SCNView!
    var scene: SCNScene!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Initialize the scene
        scene = SCNScene(named: "02773838/a55b721ea5a29d7f639ff561fa3f5bac/models/model_normalized.obj")
        
        // Setup the scene view
        sceneView = SCNView(frame: self.view.bounds)
        sceneView.scene = scene
        self.view.addSubview(sceneView)
        
        // Add camera
        let cameraNode = SCNNode()
        cameraNode.camera = SCNCamera()
        cameraNode.position = SCNVector3(x: 0, y: 0, z: 1)
        scene.rootNode.addChildNode(cameraNode)
        sceneView.pointOfView = cameraNode
        
        // Add light
        let lightNode = SCNNode()
        lightNode.light = SCNLight()
        lightNode.light!.type = .omni
        lightNode.position = SCNVector3(x: 0, y: 10, z: 10)
        scene.rootNode.addChildNode(lightNode)
        
        // Add an ambient light
        let ambientLightNode = SCNNode()
        ambientLightNode.light = SCNLight()
        ambientLightNode.light!.type = .ambient
        ambientLightNode.light!.color = NSColor.darkGray
        scene.rootNode.addChildNode(ambientLightNode)
        
        // Rotate and take screenshots
        takeScreenshotsAroundObject(cameraNode, sceneView)
    }
    
    func takeScreenshotsAroundObject(_ cameraNode: SCNNode, _ sceneView: SCNView) {
        let steps = 4
        let fullCircle: CGFloat = .pi * 2
        let stepAngle: CGFloat = fullCircle / CGFloat(steps)
        let radius: Float = 1.5

        for step in 0..<steps {
            // Calculate the angle in radians
            let angle = stepAngle * CGFloat(step)
            
            // Calculate the new camera position
            let x = radius * cos(Float(angle))
            let z = radius * sin(Float(angle))
            cameraNode.position = SCNVector3(x, Float(cameraNode.position.y), z)
            
            print(cameraNode.position)
            
            // Ensure the camera is always looking at the center of the scene
            let lookAtCenter = SCNLookAtConstraint(target: scene.rootNode)
            cameraNode.constraints = [lookAtCenter]
            
            // Wait for the scene to update
            let screenshot = sceneView.snapshot()
            self.saveImage(screenshot, withName: "screenshot\(step + 1)")
        }
    }
    
    func saveImage(_ image: NSImage, withName name: String) {
        guard let data = image.tiffRepresentation,
              let bitmapImage = NSBitmapImageRep(data: data),
              let imageData = bitmapImage.representation(using: .png, properties: [:]) else { return }
        
        let fileURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!.appendingPathComponent("\(name).png")
        
        do {
            try imageData.write(to: fileURL)
            print("Saved image to \(fileURL.path)")
        } catch {
            print("Error saving image: \(error)")
        }
    }
}
