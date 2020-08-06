#include <fstream>
#include <vector>
const int FILE_SIZE = 52428800;
typedef std::vector<char> FileBuff;

std::vector<FileBuff> GetFiles(std::string const& file_path)
{
	std::vector<FileBuff> result;
	std::ifstream file(file_path, std::ios::binary);
	char z;
	FileBuff curr;
	while (file.get(z))
	{
		curr.push_back(z);
		if (curr.size() >= FILE_SIZE)
		{
			result.push_back(curr);
			curr = {};
		}
	}
	if (curr.size())
		result.push_back(curr);
	file.close();
	return result;
}

std::string GetStr(int numb)
{
	std::string result;
	while (numb)
	{
		result += '0' + numb % 10;
		numb /= 10;
	}
	return result;
}

void WriteFiles(std::vector<FileBuff> const& files)
{
	for (int i = 0; i < files.size(); i++)
	{
		std::ofstream file(GetStr(i), std::ios::binary);
		for (char byte : files[i])
		{
			file.write(&byte, sizeof(byte));
		}
		file.close();
	}
}

int main(int argc, char* argv[])
{
	std::string filename = argv[1];
	std::vector<FileBuff> files = GetFiles(filename);
	WriteFiles(files);
	return 0;
}