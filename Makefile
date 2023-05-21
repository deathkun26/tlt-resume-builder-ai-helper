GRPC_SOURCES = ./protos/resume_builder_ai_service.py ./protos/resume_builder_ai_service_grpc.py

all: $(GRPC_SOURCES)

$(GRPC_SOURCES): ./protos/resume_builder_ai_service.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./protos/resume_builder_ai_service.proto

clean:
	rm $(GRPC_SOURCES)